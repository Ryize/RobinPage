import hashlib

import requests
from django.contrib import messages
from django.shortcuts import render

from .forms import CaptchaForm
from .models import CopySite
from .services import *


def index(request):
    """
    Главная страница ресурса. Выводит страницу с вводом сайта для копирования.
    """
    site_url = request.POST.get("site-url", False)
    captcha_form = CaptchaForm()
    if not site_url:
        return render(request, "robin/index.html", {"captcha_form": captcha_form})
    client_ip = get_client_ip(request)
    form = CaptchaForm(request.POST or None)
    if not form.is_valid():
        messages.error(request, "Вы неверно ввели капчу!")
        return render(request, "robin/index.html", {"captcha_form": captcha_form})
    if (
            check_requests_per_day(client_ip) > 4 and not request.user.is_authenticated
    ) or (check_requests_per_day(client_ip) > 15 and request.user.is_authenticated):
        messages.error(
            request,
            "Вы не можете использовать сервис так часто! Вы вновь сможете им воспользоваться завтра",
        )
        return render(request, "robin/index.html", {"captcha_form": captcha_form})
    try:
        html_data = requests.get(site_url).text
        hash_text = hashlib.sha3_512(html_data.encode("utf-8")).hexdigest()
        copy_site = CopySite(hash_text=hash_text, url=site_url)
        copy_site.save()

        add_request_from_client(client_ip)

        data = {
            "html_data": html_data,
            "hash": copy_site.hash_text
        }

        return render(
            request,
            "robin/url_page.html",
            data,
        )
    except requests.exceptions.ConnectionError:
        messages.error(request, "Превышено время ожидания подключения к серверу!")
    except (requests.exceptions.InvalidURL, requests.exceptions.MissingSchema):
        messages.error(request, "Неверный URL ресурса!")
    except Exception:
        messages.error(request, "Произошла ошибка, повторите попытку!")

    return render(request, "robin/index.html", {"captcha_form": captcha_form})


def check_site_hash(request):
    """
    Используется для проверки хеша на валидность.
    В случае успеха, возвращает информацию по хешу (url сайта, дата создания хеша);
    В случае неудачи, возвращает ошибку с помощью message.error.
    """
    if request.method == "GET":
        return render(request, "robin/check_site_hash.html")

    hash_text = request.POST.get("hash")
    if not hash_text:
        messages.error(request, "Хеш указан неверно!")
        return render(request, "robin/check_site_hash.html")
    site = CopySite.objects.filter(hash_text=hash_text).first()
    if not site:
        messages.error(request, "Сайт с таким хешем не найден!")
        return render(request, "robin/check_site_hash.html")
    return render(request, "robin/check_site_hash.html", {"site": site})

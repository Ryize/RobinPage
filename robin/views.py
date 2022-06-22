import os
import requests
import hashlib
from django.shortcuts import render, HttpResponse
from django.contrib import messages
from .forms import CaptchaForm
from .models import CopySite
from .services import *


def index(request):
    site_url = request.POST.get('site-url', False)
    captcha_form = CaptchaForm()
    if site_url:
        client_ip = get_client_ip(request)
        form = CaptchaForm(request.POST or None)
        if form.is_valid():
            if (check_requests_per_day(client_ip) > 4 and not request.user.is_authenticated) or (
                    check_requests_per_day(client_ip) > 15 and request.user.is_authenticated):
                messages.error(request,
                               'Вы не можете использовать сервис так часто! Вы вновь сможете им воспользоваться завтра')
                return render(request, 'robin/index.html', {'captcha_form': captcha_form})
            try:
                html_data = requests.get(site_url).text
                hash = hashlib.sha3_512(html_data.encode('utf-8')).hexdigest()
                copy_site = CopySite(hash_text=hash, url=site_url)
                copy_site.save()

                add_request_from_client(client_ip)
                return render(request, 'robin/url_page.html', {'html_data': html_data, 'hash': copy_site.hash_text})
            except requests.exceptions.ConnectionError:
                messages.error(request, 'Превышено время ожидания подключения к серверу!')
            except (requests.exceptions.InvalidURL, requests.exceptions.MissingSchema):
                messages.error(request, 'Неверный URL ресурса!')
            except:
                messages.error(request, 'Произошла ошибка, повторите попытку!')

        else:
            messages.error(request, 'Вы неверно ввели капчу!')

    return render(request, 'robin/index.html', {'captcha_form': captcha_form})

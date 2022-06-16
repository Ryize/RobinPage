import os
import requests
import hashlib
from django.shortcuts import render, HttpResponse
from django.contrib import messages
from .forms import CaptchaForm
from .models import CopySite


def index(request):
    site_url = request.POST.get('site-url', False)
    if site_url:
        form = CaptchaForm(request.POST or None)
        if form.is_valid():
            try:
                html_data = requests.get(site_url).text
                hash = hashlib.sha3_512(html_data.encode('utf-8')).hexdigest()
                copy_site = CopySite(hash_text=hash, url=site_url)
                copy_site.save()
                return render(request, 'robin/url_page.html', {'html_data': html_data, 'hash': copy_site.hash_text})
            except requests.exceptions.ConnectionError:
                messages.error(request, 'Превышено время ожидания подключения к серверу!')
            except (requests.exceptions.InvalidURL, requests.exceptions.MissingSchema):
                messages.error(request, 'Неверный URL ресурса!')
            # except:
            #     messages.error(request, 'Произошла ошибка, повторите попытку!')

        else:
            messages.error(request, 'Вы неверно ввели капчу!')

    captcha_form = CaptchaForm()
    return render(request, 'robin/index.html', {'captcha_form': captcha_form})

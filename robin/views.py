import requests
from django.shortcuts import render, HttpResponse
from django.contrib import messages
from .forms import CaptchaForm


def index(request):
    site_url = request.POST.get('site-url', False)
    if site_url:
        form = CaptchaForm(request.POST or None)
        if form.is_valid():
            try:
                html_data = requests.get(site_url).text
                return render(request, 'robin/url_page.html', {'html_data': html_data})
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

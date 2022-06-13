from django import forms
from captcha.fields import CaptchaField


class CaptchaForm(forms.Form):
    captcha = CaptchaField(label='Введите капчу:', error_messages={'invalid': 'Вы неверно ввели капчу!'})

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['captcha'].widget.attrs['placeholder'] = 'Капча...'

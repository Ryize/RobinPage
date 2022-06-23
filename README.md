# RobinPage

Веб-приложение для копирования любой веб-страницы. Вы "скармливаете" сайту ссылку на интересующий вас ресурс и получаете точную копию данной страницы (за небольшим исключением, сверху и снизу страницы будут кнопки для перехода на главный экран). Также в веб-приложение встроена капча и лимит дневных запросов (по умолчанию - 5, для авторизованных пользователей 15).

## Использованные технологии: 


![](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)
![](https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white)
![](https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white)
![](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)
![](https://img.shields.io/badge/JavaScript-323330?style=for-the-badge&logo=javascript&logoColor=F7DF1E)

## Развернуть проект локально:

> Установите Python (если он не установлен, рекомендуется Python 3.10)<br>
> [Download Python3](https://www.python.org/downloads/)

Клонируйте репозиторий и перейдите в папку с проектом:
```
git clone https://github.com/Ryize/RobinPage.git
cd RobinPage
```

Установите зависимости:
```
pip3 install -r requirements.txt
```

Рекомендуем изменить SECRET_KEY (для этого откройте файл RobinPage/settings.py):
```
SECRET_KEY = "Ваш SECRET_KEY"
```

Выполните миграции:
```
python3 manage.py migrate
```

Запустите сервер:
```
python3 manage.py runserver
```

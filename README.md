# WordTrainer

![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)

Приложение для изучения иностранных слов на Django.

## Особенности
- CRUD для карточек слов
- Режим тренировки с проверкой знаний
- Загрузка изображений для ассоциаций

## Установка
```bash
git clone https://github.com/Dimon777Du/WordTrainer.git
cd WordTrainer
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```
WordTrainer - Процесс создания проекта
Ниже представлен пошаговый процесс создания проекта WordTrainer с необходимыми командами и кодом:

## 1. Подготовка среды и создание проекта
bash
### Создание директории проекта
mkdir WordTrainer
cd WordTrainer

### Создание виртуального окружения
python3 -m venv venv

### Активация окружения (Linux/macOS)
source venv/bin/activate

### Активация окружения (Windows)
venv\Scripts\activate.bat

### Установка зависимостей
pip install django pillow

### Создание Django проекта
django-admin startproject wordtrainer .
## 2. Создание приложения cards
bash
python manage.py startapp cards
## 3. Настройка проекта (wordtrainer/settings.py)
python
### Добавьте в INSTALLED_APPS:
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'cards',  # Добавлено приложение cards
]

### В конец файла добавьте:
import os  # Добавьте эту строку в начало файла

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
## 4. Создание модели Card (cards/models.py)
python
from django.db import models

class Card(models.Model):
    word = models.CharField(max_length=100, verbose_name="Слово")
    translation = models.CharField(max_length=100, verbose_name="Перевод")
    image = models.ImageField(
        upload_to='images/', 
        blank=True, 
        null=True, 
        verbose_name="Изображение"
    )

    def __str__(self):
        return self.word
## 5. Создание форм (cards/forms.py)
python
from django import forms
from .models import Card

class CardForm(forms.ModelForm):
    class Meta:
        model = Card
        fields = ['word', 'translation', 'image']
        labels = {
            'word': 'Слово',
            'translation': 'Перевод',
            'image': 'Изображение'
        }
    
    def clean_word(self):
        word = self.cleaned_data.get('word')
        if not word:
            raise forms.ValidationError("Поле 'слово' не может быть пустым")
        return word
    
    def clean_translation(self):
        translation = self.cleaned_data.get('translation')
        if not translation:
            raise forms.ValidationError("Поле 'перевод' не может быть пустым")
        return translation
## 6. Создание представлений (cards/views.py)
python
from django.shortcuts import render, redirect, get_object_or_404
from .models import Card
from .forms import CardForm
import random

def home(request):
    return render(request, 'cards/home.html')

def card_list(request):
    cards = Card.objects.all()
    return render(request, 'cards/card_list.html', {'cards': cards})

def add_card(request):
    if request.method == 'POST':
        form = CardForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('card_list')
    else:
        form = CardForm()
    return render(request, 'cards/card_form.html', {'form': form})

def edit_card(request, pk):
    card = get_object_or_404(Card, pk=pk)
    if request.method == 'POST':
        form = CardForm(request.POST, request.FILES, instance=card)
        if form.is_valid():
            form.save()
            return redirect('card_list')
    else:
        form = CardForm(instance=card)
    return render(request, 'cards/card_form.html', {'form': form, 'edit': True})

def delete_card(request, pk):
    card = get_object_or_404(Card, pk=pk)
    if request.method == 'POST':
        card.delete()
        return redirect('card_list')
    return render(request, 'cards/delete_confirm.html', {'card': card})

def train(request):
    cards = list(Card.objects.all())
    card = random.choice(cards) if cards else None
    message = ''
    
    if request.method == 'POST':
        card_id = request.POST.get('card_id')
        answer = request.POST.get('answer', '').strip().lower()
        card = get_object_or_404(Card, pk=card_id)
        correct = card.translation.lower()
        
        if answer == correct:
            message = '✅ Правильно!'
        else:
            message = f'❌ Неправильно. Правильный ответ: {card.translation}'
    
    return render(request, 'cards/quiz.html', {
        'card': card,
        'message': message
    })
## 7. Настройка URL-адресов
Создайте cards/urls.py:

python
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('cards/', views.card_list, name='card_list'),
    path('cards/add/', views.add_card, name='add_card'),
    path('cards/<int:pk>/edit/', views.edit_card, name='edit_card'),
    path('cards/<int:pk>/delete/', views.delete_card, name='delete_card'),
    path('cards/train/', views.train, name='train'),
]
### Обновите wordtrainer/urls.py:

python
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('cards.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
## 8. Создание шаблонов
### Создайте структуру папок:

text
cards/
└── templates/
    └── cards/
        ├── base.html
        ├── home.html
        ├── card_list.html
        ├── card_form.html
        ├── delete_confirm.html
        └── quiz.html
### cards/templates/cards/base.html:

html
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{% block title %}WordTrainer{% endblock %}</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-light bg-light">
        <div class="container">
            <a class="navbar-brand" href="{% url 'home' %}">WordTrainer</a>
            <div class="collapse navbar-collapse">
                <ul class="navbar-nav">
                    <li class="nav-item"><a class="nav-link" href="{% url 'card_list' %}">Карточки</a></li>
                    <li class="nav-item"><a class="nav-link" href="{% url 'add_card' %}">Добавить</a></li>
                    <li class="nav-item"><a class="nav-link" href="{% url 'train' %}">Тренировка</a></li>
                </ul>
            </div>
        </div>
    </nav>

    <div class="container mt-4">
        {% block content %}{% endblock %}
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
### cards/templates/cards/home.html:

html
{% extends 'cards/base.html' %}

{% block content %}
<div class="jumbotron">
    <h1 class="display-4">Добро пожаловать в WordTrainer!</h1>
    <p class="lead">Приложение для изучения слов с помощью карточек.</p>
    <hr class="my-4">
    <p>Начните с добавления карточек, затем тренируйтесь.</p>
    <a class="btn btn-primary btn-lg" href="{% url 'card_list' %}" role="button">Управление карточками</a>
    <a class="btn btn-success btn-lg" href="{% url 'train' %}" role="button">Начать тренировку</a>
</div>
{% endblock %}
### cards/templates/cards/card_list.html:

html
{% extends 'cards/base.html' %}

{% block content %}
<h1>Список карточек</h1>
<a href="{% url 'add_card' %}" class="btn btn-primary mb-3">Добавить карточку</a>
<table class="table table-striped">
    <thead>
        <tr>
            <th>Слово</th>
            <th>Перевод</th>
            <th>Изображение</th>
            <th>Действия</th>
        </tr>
    </thead>
    <tbody>
        {% for card in cards %}
        <tr>
            <td>{{ card.word }}</td>
            <td>{{ card.translation }}</td>
            <td>
                {% if card.image %}
                <img src="{{ card.image.url }}" height="50" alt="{{ card.word }}">
                {% endif %}
            </td>
            <td>
                <a href="{% url 'edit_card' card.pk %}" class="btn btn-sm btn-warning">Редактировать</a>
                <a href="{% url 'delete_card' card.pk %}" class="btn btn-sm btn-danger">Удалить</a>
            </td>
        </tr>
        {% endfor %}
    </tbody>
</table>
{% endblock %}
### cards/templates/cards/card_form.html:

html
{% extends 'cards/base.html' %}

{% block content %}
<h1>{% if edit %}Редактировать карточку{% else %}Добавить карточку{% endif %}</h1>
<form method="post" enctype="multipart/form-data">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit" class="btn btn-primary">Сохранить</button>
    <a href="{% url 'card_list' %}" class="btn btn-secondary">Отмена</a>
</form>
{% endblock %}
### cards/templates/cards/delete_confirm.html:

html
{% extends 'cards/base.html' %}

{% block content %}
<h1>Удаление карточки</h1>
<p>Вы уверены, что хотите удалить карточку "{{ card.word }}"?</p>
<form method="post">
    {% csrf_token %}
    <button type="submit" class="btn btn-danger">Удалить</button>
    <a href="{% url 'card_list' %}" class="btn btn-secondary">Отмена</a>
</form>
{% endblock %}
### cards/templates/cards/quiz.html:

html
{% extends 'cards/base.html' %}

{% block content %}
<h1>Тренировка</h1>
{% if card %}
    <div class="card mb-3">
        {% if card.image %}
            <img src="{{ card.image.url }}" class="card-img-top" alt="{{ card.word }}" style="max-width: 300px;">
        {% endif %}
        <div class="card-body">
            <h5 class="card-title">{{ card.word }}</h5>
            <form method="post">
                {% csrf_token %}
                <input type="hidden" name="card_id" value="{{ card.id }}">
                <div class="mb-3">
                    <label for="answer" class="form-label">Введите перевод:</label>
                    <input type="text" class="form-control" id="answer" name="answer" required>
                </div>
                <button type="submit" class="btn btn-primary">Проверить</button>
            </form>
            {% if message %}
                <div class="alert alert-info mt-3">{{ message }}</div>
                <a href="{% url 'train' %}" class="btn btn-secondary">Следующее слово</a>
            {% endif %}
        </div>
    </div>
{% else %}
    <div class="alert alert-warning">Нет карточек для тренировки. Пожалуйста, добавьте карточки.</div>
{% endif %}
{% endblock %}
## 9. Запуск проекта
bash
### Создание миграций
python manage.py makemigrations

### Применение миграций
python manage.py migrate

### Запуск сервера разработки
python manage.py runserver
10. Тестирование приложения
Откройте в браузере:
http://localhost:8000/ - Главная страница
http://localhost:8000/cards/ - Список карточек
http://localhost:8000/cards/add/ - Добавление карточки
http://localhost:8000/cards/train/ - Тренировка

### Применение миграций
python manage.py migrate

### Запуск сервера
python manage.py runserver

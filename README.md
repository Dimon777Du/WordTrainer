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

# WordTrainer - Проект для изучения иностранных слов

## Этапы создания проекта

### 1. Подготовка среды разработки
```bash
# Создание директории проекта
mkdir WordTrainer
cd WordTrainer

# Создание виртуального окружения
python3 -m venv venv
source venv/bin/activate

# Установка зависимостей
pip install django pillow
```

### 2. Инициализация Django-проекта
```bash
django-admin startproject wordtrainer .
```

### 3. Создание приложения cards
```bash
python manage.py startapp cards
```

### 4. Настройка проекта (wordtrainer/settings.py)
```python
# Добавляем приложение в INSTALLED_APPS
INSTALLED_APPS = [
    ...
    'cards',
]

# Добавляем настройки для медиафайлов
import os

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
```

### 5. Настройка URL-адресов (wordtrainer/urls.py)
```python
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('cards.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

### 6. Создание модели Card (cards/models.py)
```python
from django.db import models

class Card(models.Model):
    word = models.CharField(max_length=100)
    translation = models.CharField(max_length=100)
    image = models.ImageField(upload_to='images/', blank=True, null=True)

    def __str__(self):
        return self.word
```

### 7. Создание формы (cards/forms.py)
```python
from django import forms
from .models import Card

class CardForm(forms.ModelForm):
    class Meta:
        model = Card
        fields = ['word', 'translation', 'image']
    
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
```

### 8. Реализация представлений (cards/views.py)
```python
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
        answer = request.POST.get('answer', '').strip().lower()
        correct = request.POST.get('correct', '').strip().lower()
        if answer == correct:
            message = '✅ Правильно!'
        else:
            message = f'❌ Неправильно. Правильный ответ: {correct}'
    return render(request, 'cards/quiz.html', {'card': card, 'message': message})
```

### 9. Настройка URL-адресов приложения (cards/urls.py)
```python
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
```

### 10. Создание базового шаблона (cards/templates/cards/base.html)
```html
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{% block title %}WordTrainer{% endblock %}</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body { padding-top: 20px; }
        .card-image { max-height: 150px; object-fit: contain; }
    </style>
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-light bg-light mb-4">
        <div class="container">
            <a class="navbar-brand" href="{% url 'home' %}">WordTrainer</a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav">
                    <li class="nav-item">
                        <a class="nav-link" href="{% url 'card_list' %}">Карточки</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="{% url 'add_card' %}">Добавить слово</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="{% url 'train' %}">Тренировка</a>
                    </li>
                </ul>
            </div>
        </div>
    </nav>

    <div class="container">
        {% block content %}{% endblock %}
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
```

### 11. Главная страница (cards/templates/cards/home.html)
```html
{% extends 'cards/base.html' %}

{% block content %}
<div class="text-center">
    <h1 class="display-4">Добро пожаловать в WordTrainer!</h1>
    <p class="lead">Приложение для изучения иностранных слов</p>
    <div class="mt-5">
        <a href="{% url 'card_list' %}" class="btn btn-primary btn-lg mx-2">Просмотреть слова</a>
        <a href="{% url 'add_card' %}" class="btn btn-success btn-lg mx-2">Добавить слово</a>
        <a href="{% url 'train' %}" class="btn btn-warning btn-lg mx-2">Начать тренировку</a>
    </div>
</div>
{% endblock %}
```

### 12. Страница списка карточек (cards/templates/cards/card_list.html)
```html
{% extends 'cards/base.html' %}

{% block content %}
<h1 class="mb-4">Список карточек</h1>
<a href="{% url 'add_card' %}" class="btn btn-primary mb-3">Добавить карточку</a>

<div class="table-responsive">
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
</div>
{% endblock %}
```

### 13. Форма добавления/редактирования (cards/templates/cards/card_form.html)
```html
{% extends 'cards/base.html' %}

{% block content %}
<h1 class="mb-4">
    {% if edit %}Редактирование карточки{% else %}Добавление новой карточки{% endif %}
</h1>

<form method="post" enctype="multipart/form-data">
    {% csrf_token %}
    
    <div class="mb-3">
        <label for="id_word" class="form-label">Слово</label>
        {{ form.word }}
        {% if form.word.errors %}
            <div class="text-danger">{{ form.word.errors }}</div>
        {% endif %}
    </div>
    
    <div class="mb-3">
        <label for="id_translation" class="form-label">Перевод</label>
        {{ form.translation }}
        {% if form.translation.errors %}
            <div class="text-danger">{{ form.translation.errors }}</div>
        {% endif %}
    </div>
    
    <div class="mb-3">
        <label for="id_image" class="form-label">Изображение (необязательно)</label>
        {{ form.image }}
        {% if form.image.errors %}
            <div class="text-danger">{{ form.image.errors }}</div>
        {% endif %}
    </div>
    
    <button type="submit" class="btn btn-primary">
        {% if edit %}Сохранить изменения{% else %}Добавить карточку{% endif %}
    </button>
    <a href="{% url 'card_list' %}" class="btn btn-secondary">Отмена</a>
</form>
{% endblock %}
```

### 14. Подтверждение удаления (cards/templates/cards/delete_confirm.html)
```html
{% extends 'cards/base.html' %}

{% block content %}
<h1 class="mb-4">Удаление карточки</h1>
<p>Вы уверены, что хотите удалить карточку <strong>"{{ card.word }}"</strong>?</p>

<form method="post">
    {% csrf_token %}
    <button type="submit" class="btn btn-danger">Да, удалить</button>
    <a href="{% url 'card_list' %}" class="btn btn-secondary">Отмена</a>
</form>
{% endblock %}
```

### 15. Страница тренировки (cards/templates/cards/quiz.html)
```html
{% extends 'cards/base.html' %}

{% block content %}
<h1 class="mb-4">Тренировка слов</h1>

{% if card %}
<div class="card mb-4">
    <div class="card-body text-center">
        {% if card.image %}
        <img src="{{ card.image.url }}" class="card-image mb-3" alt="{{ card.word }}">
        {% endif %}
        
        <h2 class="card-title">{{ card.word }}</h2>
        
        <form method="post" class="mt-4">
            {% csrf_token %}
            <input type="hidden" name="correct" value="{{ card.translation }}">
            
            <div class="mb-3">
                <label for="answer" class="form-label">Введите перевод:</label>
                <input type="text" name="answer" id="answer" class="form-control" required autofocus>
            </div>
            
            <button type="submit" class="btn btn-primary">Проверить</button>
            <a href="{% url 'train' %}" class="btn btn-secondary">Следующее слово</a>
        </form>
        
        {% if message %}
        <div class="alert {% if 'Правильно' in message %}alert-success{% else %}alert-danger{% endif %} mt-3">
            {{ message }}
        </div>
        {% endif %}
    </div>
</div>
{% else %}
<div class="alert alert-warning">
    Нет доступных карточек для тренировки. Пожалуйста, добавьте слова.
</div>
{% endif %}

<div class="text-center">
    <a href="{% url 'card_list' %}" class="btn btn-outline-secondary">Вернуться к списку</a>
</div>
{% endblock %}
```

### 16. Запуск миграций и сервера
```bash
# Создание миграций
python manage.py makemigrations

# Применение миграций
python manage.py migrate

# Создание суперпользователя (опционально)
python manage.py createsuperuser

# Запуск сервера разработки
python manage.py runserver
```

### 17. Тестирование приложения
Откройте в браузере:
- http://localhost:8000/ - Главная страница
- http://localhost:8000/cards/ - Список карточек
- http://localhost:8000/cards/add/ - Добавление карточки
- http://localhost:8000/cards/train/ - Тренировка слов

## Функциональность приложения
1. **Главная страница**:
   - Краткое описание приложения
   - Навигация по основным разделам

2. **Управление карточками**:
   - Добавление новых слов с переводом и изображением
   - Редактирование существующих карточек
   - Удаление карточек с подтверждением
   - Просмотр всех карточек в виде таблицы

3. **Тренировка слов**:
   - Случайный выбор слова для перевода
   - Проверка введенного перевода
   - Визуальная обратная связь (правильно/неправильно)
   - Возможность перейти к следующему слову

## Используемые технологии
- Backend: Django 4.2
- Frontend: HTML5, CSS3, Bootstrap 5
- База данных: SQLite
- Дополнительные библиотеки: Pillow (для работы с изображениями)

Проект полностью готов к использованию и соответствует всем поставленным требованиям.

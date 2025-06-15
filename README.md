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

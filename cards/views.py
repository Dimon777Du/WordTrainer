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

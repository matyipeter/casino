from django.shortcuts import render, redirect
import numpy as np
from numpy import random
from user.models import UserProfile
from django.contrib import messages


# Helper function
def spin(bet):
    slots = [['cherry','cherry','cherry','cherry','cherry','banana', 'banana','helicopter','bird','bird'],
             ['cherry','cherry','cherry','cherry','banana','banana','banana','helicopter','helicopter','bird'],
             ['cherry','cherry','cherry','cherry','cherry','banana','banana','helicopter','bird','bird']]
    winner_symbols = [random.choice(slots[0]), random.choice(slots[1]), random.choice(slots[2])]
    print(winner_symbols)
    if all(i == winner_symbols[0] for i in winner_symbols) and winner_symbols[0] == 'cherry':
        return bet * 6
    elif all(i == winner_symbols[0] for i in winner_symbols) and winner_symbols[0] == 'helicopter':
        return bet*20
    else:
        return 0


def game(request, bet):
    # IMPORTANT note
    # user.save() is always needed because we have to save the current changes to the database

    # getting the current user
    user = UserProfile.objects.get(user=request.user)
    print(user.user.username)
    
    # taking the bet away from the users balance with conditions
    if user.balance - bet < 0:
        print('Cant fund')
        return redirect('games:slot')
    else:
        user.balance -= bet
        user.save()
    
    # spinning the slot machine and evaluating
    win = spin(bet)
    print(win)
    
    # adding the win to the users balance (can be 0 if he didnt win)
    user.balance += win
    user.save()
    
    return redirect('games:slot')

def slot(request):

    try:
        user = UserProfile.objects.get(user=request.user)

    except:
        messages.info(request, 'You have to log in to play games.') 
        return redirect('/')

    if request.method == 'POST':
        data = request.POST
        bet = int(data['bet'])
        print(bet)
    else:
        bet = 0
    
    return render(request, 'games/slot.html', {'balance':user.balance, 'bet': bet})

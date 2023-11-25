from django.shortcuts import render, redirect
import numpy as np
from numpy import random
from user.models import UserProfile


# Create your views here.


def spin(bet, pattern):

    baseMultiplier = 11
    winning_numbers = random.choice(pattern, size=(3))
    print(winning_numbers)
    if winning_numbers[0] == winning_numbers[1] and winning_numbers[0] == winning_numbers[2]:
        return bet * (baseMultiplier-winning_numbers[0])
    else:
        return 0
    
def game(request):
    # IMPORTANT note
    # user.save() is always needed because we have to save the current changes to the database


    # CHANGES NEEDED
    patterns = random.choice([1,2,3,4,5,6], p=[0.005, 0.095, 0.15, 0.20, 0.25, 0.3], size=1000)
    bet = 20
    
    # getting the current user
    user = UserProfile.objects.get(user=request.user)
    print(user.user.username)
    
    # taking the bet away from the users balance
    user.balance -= bet
    user.save()
    
    # spinning the slot machine and evaluating
    win = spin(bet, patterns)
    print(win)
    
    # adding the win to the users balance (can be 0 if he didnt win)
    user.balance += win
    user.save()
    
    return redirect('games:slot')

def slot(request):

    user = UserProfile.objects.get(user=request.user)
    
    return render(request, 'games/slot.html', {'balance':user.balance})

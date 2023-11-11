from django.shortcuts import render, redirect
from .forms import UserCreateForm, UserProfileForm, MoneyInputForm
from django.contrib import messages
from django.contrib.auth import get_user_model
from .models import UserProfile, TransactionHistory, WinningHistory
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes,force_str
from django.core.mail import EmailMessage
from .tokens import account_activation_token
from datetime import datetime
from django.contrib.auth.decorators import login_required


def index(request):
    # HOME PAGE
    return render(request, "user/index.html")

# Function to activate the user account based on the token and UID
def activate(request, uidb64, token):
    User = UserProfile  # Get the user model
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))  # Decode the UID
        user = User.objects.get(pk=uid)  # Get the user based on the UID
    except:
        user = None  # Set the user to None if there's an error during retrieval
    
    # Check if the user is not None and the token is valid
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True  # Set the user's account as active
        user.save()  # Save the user's updated status
        print('EMAIL VERIFIED!')  # Print a success message to the console
        return redirect('index')  # Redirect to the 'index' page after successful activation

    return redirect('index')  # Redirect to the 'index' page if the activation is not successful


# Function to send the activation email
def activate_email(request, user, to_email):
    # Define the email subject
    mail_subject = "Activate your user account"

    # Render the email message template with necessary context variables
    message = render_to_string("user/template_activate_account.html", {
        'user': user.username,
        'domain': get_current_site(request).domain,  # Get the current domain
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),  # Encode the user's primary key
        'token': account_activation_token.make_token(user),  # Generate the account activation token
        'protocol': 'https' if request.is_secure() else 'http',  # Define the protocol based on request security
    })

    # Create an EmailMessage object
    email = EmailMessage(mail_subject, message, to=[to_email])

    # Send the email and handle the success or failure
    if email.send():
        print('Successful email sending')
    else:
        print('FAIL')

    # Provide a success message to the user on the website
    messages.success(request, f'Dear <b>{user}</b>, please check your email sent to <b>{to_email}</b> and confirm the activation link to complete the registration.')
    

# Function for user registration
def register(request):
    # Check if the HTTP method is POST
    if request.method == 'POST':
        form = UserCreateForm(request.POST)  # Instantiate the user creation form with the posted data
        profile_form = UserProfileForm(request.POST)
        # Check if the form data is valid
        if form.is_valid() and profile_form.is_valid():
            user = form.save(commit=False)  # Save the form data without committing to the database
            user.set_password(user.password) 
            user.is_active = False  # Set the user's account status as inactive 
            user.save()  # Save the user to the database
            activate_email(request, user, form.cleaned_data.get('email'))  # Send an activation email
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            return redirect('/')  # Redirect to the home page after successful registration
    else:
        form = UserCreateForm()  # Instantiate an empty user creation form
        profile_form = UserProfileForm()
    
    return render(request, 'user/register.html', {'form': form, 'profileform':profile_form})  # Render the registration template with the form

@login_required
def account(request):
    user_profile = UserProfile.objects.get(user=request.user)
    transactions = user_profile.transactionhistory_set.all().order_by('-transaction_date')[:10]
    return render(request, 'user/account.html',{'userp':user_profile, 'transactions': transactions})


def password_change_done(request):
    return render(request, 'user/password_change_done.html')


def deposit(request):

    if request.method == 'POST':
        form = MoneyInputForm(request.POST)

        if form.is_valid():
            flow = form.cleaned_data['money']
            user = UserProfile.objects.get(user=request.user)
            if flow > 0:
                new_trans = TransactionHistory(user=user, flow=flow, transaction_date=datetime.now())           
                new_trans.save()
                return redirect('user:account')
            else:
                print('Cannot add negative amount')
            
    else:
        form = MoneyInputForm()
    
    return render(request, 'user/deposit.html', {'form':form})


def withdraw(request):

    if request.method == 'POST':
        form = MoneyInputForm(request.POST)

        if form.is_valid():
            flow = form.cleaned_data['money']
            user = UserProfile.objects.get(user=request.user)
            if flow > 0:
                if user.balance - flow >= 0:
                    flow = flow * -1
                    new_trans = TransactionHistory(user=user, flow=flow, transaction_date=datetime.now())           
                    new_trans.save()
                    return redirect('user:account')
                else:
                    print('Cannot withdraw more then available')
            else:
                print('Cannot withdraw negative amount')
            
    else:
        form = MoneyInputForm()
    
    return render(request, 'user/withdraw.html', {'form':form})



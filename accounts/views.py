from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from accounts.models import SarataniUser
from .forms import UserRegisterForm, UserUpdateForm
from django.contrib.auth import login, authenticate


def login_user(request):
    context = dict()
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Logged In')
            return redirect('predictions')
        else:
            context['username'] = username
            context['password'] = password
            context['invalid'] = True
    return render(request, 'accounts/login.html', context)

def register(request):
    """To Create a Users Account."""
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            login(request, new_user)
            messages.success(request, 'Your account has been created. Welcome to Saratani Ai.')
            return redirect('/')
    else:
        form = UserRegisterForm()
    return render(request, 'accounts/register.html', {'form': form})


# This method is to show the users profile when they login
@login_required
def edit_profile(request):
    """To edit a users profile when he logs in and chooses to edit."""
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        #p_form = ProfileUpdateForm(request.POST,
                                   #request.FILES,
                                   #instance=request.user.profile)

        if u_form.is_valid():
            u_form.save()
            #p_form.save()
            messages.success(request, f'Your account has been Updated.')
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        #p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form
        #'p_form': p_form
    }
    return render(request, 'accounts/edit_profile.html', context)


@login_required
def profile(request):
    """To edit a users profile when he logs in."""
    return render(request, 'accounts/profile.html')

@login_required
def view_profile(request, kiongozi):
    context = {'mtu': get_object_or_404(SarataniUser, user=request.user)}
    template = "accounts/view-profile.html"
    return render(request, template, context)
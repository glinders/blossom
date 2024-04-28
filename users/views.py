from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, (
                f'The account for {username} has been created.'''
                ' You are now able to log in.'
            ))
            return redirect('users:login')
    else:
        # create an empty form
        form = UserRegisterForm()
    data = {'form': form}
    return render(request, 'users/register.html', data)


@login_required
def profile(request):
    return render(request, 'users/profile.html')

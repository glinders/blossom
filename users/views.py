from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.conf import settings
from .forms import (
    UserRegisterForm, UserUpdateForm, ProfileUpdateForm,
)


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        # we require a token when registering
        if (
                form.is_valid() and
                form.data['register_token'] == settings.USER_REGISTER_TOKEN
        ):
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(
                request,
                (
                    f'The account for {username} has been created.'
                    ' You are now able to log in.'
                ),
            )
            return redirect('users:login')
        else:
            messages.error(
                request,
                (
                    f'Invalid data. You were not registered.'
                ),
            )
            return redirect('users:login')
    else:
        # create an empty form
        form = UserRegisterForm()
    context = {
        'title': 'Register',
        'form': form,
    }
    return render(request, 'users/register.html', context)


@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(
            request.POST,
            request.FILES,  # user profile image
            instance=request.user.profile
        )
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            username = u_form.cleaned_data.get('username')
            messages.success(
                request,
                f'The account for {username} has been updated.',
            )
            return redirect('users:profile')
    else:
        # populate user form with current user's data
        u_form = UserUpdateForm(instance=request.user)
        # populate profile form with current user's profile
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'title': 'Profile',
        'u_form': u_form,
        'p_form': p_form,
    }
    return render(request, 'users/profile.html', context)

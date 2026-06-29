from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegisterForm, ProfileForm, AdminUserEditForm
from .models import User
from legoshop.orders.models import Order


def register_view(request):
    if request.user.is_authenticated:
        return redirect('catalog:index')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Welcome, {user.username}! Your account has been created.')
            return redirect('catalog:index')
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('catalog:index')
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            next_url = request.GET.get('next', 'catalog:index')
            return redirect(next_url)
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    if request.method == 'POST':
        logout(request)
        messages.info(request, 'You have been logged out.')
    return redirect('catalog:index')


@login_required
def profile_view(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('accounts:profile')
    else:
        form = ProfileForm(instance=request.user)
    orders = Order.objects.filter(user=request.user).order_by('-created_at')[:5]
    return render(request, 'accounts/profile.html', {'form': form, 'orders': orders})


# ─── Admin-only views ────────────────────────────────────────────────────────

def admin_required(view_func):
    """Decorator: only shop admins can access."""
    from functools import wraps
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_shop_admin():
            messages.error(request, 'Access denied.')
            return redirect('catalog:index')
        return view_func(request, *args, **kwargs)
    return wrapper


@login_required
@admin_required
def admin_users_list(request):
    users = User.objects.all().order_by('date_joined')
    return render(request, 'accounts/admin_users.html', {'users': users})


@login_required
@admin_required
def admin_user_edit(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        form = AdminUserEditForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, f'User {user.username} updated.')
            return redirect('accounts:admin_users')
    else:
        form = AdminUserEditForm(instance=user)
    return render(request, 'accounts/admin_user_edit.html', {'form': form, 'edited_user': user})


@login_required
@admin_required
def admin_user_delete(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        username = user.username
        user.delete()
        messages.success(request, f'User {username} deleted.')
        return redirect('accounts:admin_users')
    return render(request, 'accounts/admin_user_confirm_delete.html', {'edited_user': user})

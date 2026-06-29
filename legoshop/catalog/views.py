from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Product, Category
from .forms import ProductForm, CategoryForm, ProductSearchForm
from legoshop.accounts.views import admin_required


def index(request):
    form = ProductSearchForm(request.GET)
    products = Product.objects.filter(is_available=True)
    categories = Category.objects.all()

    if form.is_valid():
        q = form.cleaned_data.get('q')
        category = form.cleaned_data.get('category')
        min_price = form.cleaned_data.get('min_price')
        max_price = form.cleaned_data.get('max_price')

        if q:
            products = products.filter(Q(name__icontains=q) | Q(description__icontains=q))
        if category:
            products = products.filter(category=category)
        if min_price is not None:
            products = products.filter(price__gte=min_price)
        if max_price is not None:
            products = products.filter(price__lte=max_price)

    return render(request, 'catalog/index.html', {
        'products': products,
        'categories': categories,
        'form': form,
    })


def category_view(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(category=category, is_available=True)
    return render(request, 'catalog/category.html', {'category': category, 'products': products})


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    return render(request, 'catalog/product_detail.html', {'product': product})


# ─── Admin Product Management ─────────────────────────────────────────────────

@login_required
@admin_required
def admin_product_list(request):
    products = Product.objects.all().select_related('category')
    return render(request, 'catalog/admin_product_list.html', {'products': products})


@login_required
@admin_required
def admin_product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            messages.success(request, f'Product "{product.name}" created.')
            return redirect('catalog:admin_product_list')
    else:
        form = ProductForm()
    return render(request, 'catalog/admin_product_form.html', {'form': form, 'action': 'Create'})


@login_required
@admin_required
def admin_product_edit(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, f'Product "{product.name}" updated.')
            return redirect('catalog:admin_product_list')
    else:
        form = ProductForm(instance=product)
    return render(request, 'catalog/admin_product_form.html', {'form': form, 'action': 'Edit', 'product': product})


@login_required
@admin_required
def admin_product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        name = product.name
        product.delete()
        messages.success(request, f'Product "{name}" deleted.')
        return redirect('catalog:admin_product_list')
    return render(request, 'catalog/admin_product_confirm_delete.html', {'product': product})


# ─── Admin Category Management ────────────────────────────────────────────────

@login_required
@admin_required
def admin_category_list(request):
    categories = Category.objects.all()
    return render(request, 'catalog/admin_category_list.html', {'categories': categories})


@login_required
@admin_required
def admin_category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            category = form.save()
            messages.success(request, f'Category "{category.name}" created.')
            return redirect('catalog:admin_category_list')
    else:
        form = CategoryForm()
    return render(request, 'catalog/admin_category_form.html', {'form': form, 'action': 'Create'})


@login_required
@admin_required
def admin_category_edit(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, f'Category "{category.name}" updated.')
            return redirect('catalog:admin_category_list')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'catalog/admin_category_form.html', {'form': form, 'action': 'Edit', 'category': category})


@login_required
@admin_required
def admin_category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        name = category.name
        category.delete()
        messages.success(request, f'Category "{name}" deleted.')
        return redirect('catalog:admin_category_list')
    return render(request, 'catalog/admin_category_confirm_delete.html', {'category': category})

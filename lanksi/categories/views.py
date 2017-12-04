from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib.auth.decorators import login_required
from categories.models import Category
from categories.forms import CategoryForm, EditCategoryForm


@login_required
def list_(request):
    categories = Category.objects.filter(owner=request.user)
    return render(request, 'categories/list_.html', {'categories': categories})


@login_required
def add(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            new_cat = form.save(commit=False)
            new_cat.owner = request.user
            new_cat.save()
            return redirect(reverse("categories:list_"))
    else:
        form = CategoryForm()
    return render(request, 'categories/add.html', {'form': form})


@login_required
def details(request, slug):
    category = get_object_or_404(Category, slug=slug, owner=request.user)
    return render(request, "categories/details.html", {'category': category})


@login_required
def edit(request, slug):
    category = get_object_or_404(Category, slug=slug, owner=request.user)
    if request.method == 'POST':
        form = EditCategoryForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            Category.objects.create(cat_type=cd['cat_type'],
                                    name=cd['name'],
                                    owner=request.user)
            category.delete()

            return redirect(reverse("categories:list_"))
    else:
        form = EditCategoryForm(initial={'cat_type': category.cat_type,
                                         'name': category.name})
    return render(request, "categories/edit.html", {'category': category,
                                                    'form': form})


@login_required
def delete(request, slug):
    category = get_object_or_404(Category, slug=slug, owner=request.user)
    return render(request, 'categories/delete.html', {'category': category})


@login_required
def confirm_delete(request, slug):
    category = get_object_or_404(Category, slug=slug, owner=request.user)
    category.delete()
    return redirect(reverse("categories:list_"))

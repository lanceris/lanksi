from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from patterns.models import TransactionTemplate
from  patterns.forms import PatternForm

@login_required
def list_(request):
    patterns = TransactionTemplate.objects.filter(owner=request.user)
    return render(request, 'patterns/list_.html', {'patterns': patterns})


@login_required
def add(request, transaction=None):
    if request.method == 'POST':
        form = PatternForm(request.POST, transaction=transaction)
        if form.is_valid():
            new_pat = form.save(commit=False)
            new_pat.owner = request.user
            new_pat.save()
            return redirect(reverse("patterns:list_"))
    else:
        form = PatternForm(transaction=transaction)
    return render(request, 'patterns/add.html', {'form': form})


@login_required
def edit(request, id):
    pattern = TransactionTemplate.objects.get(id=id, owner=request.user)
    if request.method == 'POST':
        form = PatternForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            PatternForm.objects.create(owner=request.user,
                                       name=cd['name'],
                                       transaction=cd['transaction'],
                                       description=cd['description'])
            pattern.delete()

            return redirect(reverse("patterns:list_"))
    else:
        form = PatternForm(initial={'name': pattern.name,
                                    'transaction': pattern.transaction,
                                    'description': pattern.description})
    return render(request, "patterns/edit.html", {'pattern': pattern,
                                                  'form': form})


@login_required
def delete(request, id):
    pattern = TransactionTemplate.objects.get(id=id, owner=request.user)
    return render(request, 'patterns/delete.html', {'pattern': pattern})


@login_required
def confirm_delete(request, id):
    pattern = TransactionTemplate.objects.get(id=id, owner=request.user)
    pattern.delete()
    return redirect(reverse("patterns:list_"))
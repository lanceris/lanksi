from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from patterns.models import TransactionTemplate
from  patterns.forms import PatternForm, PatternEditForm
from accounts.models import Transaction
@login_required
def list_(request):
    patterns = TransactionTemplate.objects.filter(owner=request.user)
    return render(request, 'patterns/list_.html', {'patterns': patterns})


@login_required
def add(request):
    if request.method == 'POST':
        try:
            form = PatternForm(request.POST, owner=request.user,
                               transaction=Transaction.objects.get(id=request.GET.get('trans_id')))
        except:
            form = PatternForm(request.POST, owner=request.user,
                               transaction=Transaction.objects.none())

        if form.is_valid():
            cd = form.cleaned_data
            try:
                transaction = Transaction.objects.get(id=request.GET.get('trans_id'))
            except:
                transaction = cd['transaction']
            TransactionTemplate.objects.create(owner=request.user,
                                               name=cd['name'],
                                               transaction=transaction,
                                               description=cd['description'])
            return redirect(reverse("patterns:list_"))
    else:
        try:
            form = PatternForm(owner=request.user,
                               transaction=Transaction.objects.get(id=request.GET.get('trans_id')))
        except:
            form = PatternForm(owner=request.user,
                               transaction=Transaction.objects.none())
    return render(request, 'patterns/add.html', {'form': form})


@login_required
def edit(request, id):
    pattern = TransactionTemplate.objects.get(id=id, owner=request.user)
    if request.method == 'POST':
        form = PatternEditForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            TransactionTemplate.objects.create(owner=request.user,
                                               name=cd['name'],
                                               transaction=cd['transaction'],
                                               description=cd['description'])
            pattern.delete()

            return redirect(reverse("patterns:list_"))
    else:
        form = PatternEditForm(initial={'name': pattern.name,
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
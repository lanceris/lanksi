from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required

from goals.models import Goal


# Goals views
@login_required
def list_(request):
    goals = Goal.objects.filter(owner=request.user)

    return render(request, 'list_.html', {'goals': goals,
                                          'form': form,
                                          'history': history_items})


@login_required
def add(request):
    if request.method == 'POST':
        form = BankAccountForm(request.POST)
        if form.is_valid():
            new_acc = form.save(commit=False)
            new_acc.owner = request.user
            new_acc.save()
            return redirect(reverse("accounts:list_"))
    else:
        form = BankAccountForm()
    return render(request, 'add.html', {'form': form})


@login_required
def details(request, slug):
    account = get_object_or_404(BankAccount, slug=slug, owner=request.user)
    return render(request, "details.html", {'account': account})


@login_required
def edit(request, slug):
    account = BankAccount.objects.get(slug=slug, owner=request.user)
    if request.method == 'POST':
        form = BankAccountEditForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            BankAccount.objects.create(label=cd['label'],
                                       currency=account.currency,
                                       balance=account.balance,
                                       owner=request.user,
                                       description=cd['description'])
            account.delete()

            return redirect(reverse("accounts:list_"))
    else:
        form = BankAccountEditForm(initial={'label': account.label,
                                            'description': account.description})
    return render(request, "edit.html", {'account': account,
                                                     'form': form})


@login_required
def delete(request, slug):
    account = BankAccount.objects.get(slug=slug, owner=request.user)
    return render(request, 'delete.html', {'account': account})


@login_required
def confirm_delete(request, slug):
    account = BankAccount.objects.get(slug=slug, owner=request.user)
    account.delete()
    return redirect(reverse("accounts:list"))
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.conf import settings
from django.views.generic import TemplateView

from .models import BankAccount, Transaction
from .forms import TransactionForm, MoveMoneyForm,\
                    FilterHistoryForm, AddBankAccountForm, \
                    EditBankAccountForm


class IndexView(TemplateView):
    template_name = 'index.html'


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(reverse('login'))
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


#region accounts
def get_history(accounts, queryset):
    history_items = []
    for t in queryset:
        item = {'type': None, 'description': t.comment, 'datetime': t.created, 'tag': 'TODO',
                'debit': '', 'credit': '', 'from': '', 'to': ''}
        if t.tr_type == settings.TR_ADD:
            item['type'] = 1
            item['credit'] = t.tr_amount
            item['balance'] = t.balance
            item['balance_before'] = t.balance - t.tr_amount
        elif t.tr_type == settings.TR_WITHDRAW:
            item['type'] = 2
            item['debit'] = t.tr_amount
            item['balance'] = t.balance
            item['balance_before'] = t.balance + t.tr_amount
        elif t.tr_type == settings.TR_MOVE:
            item['type'] = 3
            if t.tr_from in accounts:
                item['debit'] = t.tr_amount
                item['balance'] = t.balance
                item['to'] = t.tr_from
                item['from'] = t.tr_to
                item['balance_before'] = t.balance + t.tr_amount
            else:
                item['credit'] = t.tr_amount
                item['balance'] = t.recipient_balance
                item['from'] = t.tr_from
                item['balance_before'] = t.recipient_balance - t.tr_amount
        elif t.tr_type == settings.TR_EXCHANGE:
            item['type'] = 4

            #TODO: exchange logic
            pass
        history_items.append(item)

    return history_items


@login_required
def list_(request):
    accounts = BankAccount.objects.filter(owner=request.user)
    from django.db.models import Q
    queryset = Transaction.objects.filter(
        Q(tr_from__in=accounts) | Q(tr_to__in=accounts)).order_by('-created')

    if request.method == 'POST':
        form = FilterHistoryForm(request.POST, request=request)
        if form.is_valid():
            if form.cleaned_data['time_period']:
                queryset = queryset.filter(created__gte=form.cleaned_data['time_period'])
            if form.cleaned_data['date_from']:
                queryset = queryset.filter(created__gte=form.cleaned_data['date_from'])
            if form.cleaned_data['date_to']:
                queryset = queryset.filter(created__lte=form.cleaned_data['date_to'])
            if form.cleaned_data['keywords']:
                queryset = queryset.filter(comment__contains=form.cleaned_data['keywords'])
            if form.cleaned_data['account']:
                queryset = queryset.filter(Q(tr_from=form.cleaned_data['account']))
            if form.cleaned_data['category']:
                queryset = queryset.filter(category=form.cleaned_data['category'])
    else:
        form = FilterHistoryForm(request=request)

    history_items = get_history(accounts=accounts,
                                queryset=queryset)
    return render(request, 'accounts/list_.html', {'accounts': accounts,
                                          'form': form,
                                          'history': history_items})


@login_required
def add(request):
    if request.method == 'POST':
        form = AddBankAccountForm(request.POST)
        if form.is_valid():
            new_acc = form.save(commit=False)
            new_acc.owner = request.user
            new_acc.save()
            return redirect(reverse("accounts:list_"))
    else:
        form = AddBankAccountForm()
    return render(request, 'accounts/add.html', {'form': form})


@login_required
def details(request, slug):
    account = get_object_or_404(BankAccount, slug=slug, owner=request.user)
    return render(request, "accounts/details.html", {'account': account})


@login_required
def edit(request, slug):
    account = BankAccount.objects.get(slug=slug, owner=request.user)
    if request.method == 'POST':
        form = EditBankAccountForm(request.POST)
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
        form = EditBankAccountForm(initial={'label': account.label,
                                            'description': account.description})
    return render(request, "accounts/edit.html", {'account': account,
                                         'form': form})


@login_required
def delete(request, slug):
    account = BankAccount.objects.get(slug=slug, owner=request.user)
    return render(request, 'accounts/delete.html', {'account': account})


@login_required
def confirm_delete(request, slug):
    account = BankAccount.objects.get(slug=slug, owner=request.user)
    account.delete()
    return redirect(reverse("accounts:list_"))
#endregion accounts


#region operations
@login_required
def add_money(request, slug):
    account = get_object_or_404(BankAccount, slug=slug, owner=request.user)
    if request.method == 'POST':
        form = TransactionForm(request.POST, request=request, cat_type=settings.TR_ADD)
        if form.is_valid():
            cd = form.cleaned_data
            account.add_money(amount=cd['amount'],
                              tag=cd['tag'],
                              category=cd['category'],
                              description=cd['description'])
            return redirect(reverse("accounts:details", args=[account.slug]))
    else:
        form = TransactionForm(request=request, cat_type=settings.TR_ADD)
    return render(request, "accounts/money_transfer.html", {'account': account,
                                                            'form': form,
                                                            'msg': 'Add money'})


@login_required
def withdraw_money(request, slug):
    account = get_object_or_404(BankAccount, slug=slug, owner=request.user)
    if request.method == 'POST':
        form = TransactionForm(request.POST, request=request, cat_type=settings.TR_WITHDRAW)
        if form.is_valid():
            cd = form.cleaned_data
            account.withdraw_money(amount=cd['amount'],
                                   tag=cd['tag'],
                                   category=cd['category'],
                                   description=cd['description'])
            return redirect(reverse("accounts:details", args=[account.slug]))
    else:
        form = TransactionForm(request=request, cat_type=settings.TR_WITHDRAW)
    return render(request, "accounts/money_transfer.html", {'account': account,
                                                            'form': form,
                                                            'msg': 'Withdraw money'})


@login_required
def move_money(request, slug):
    account = get_object_or_404(BankAccount, slug=slug, owner=request.user)
    if request.method == 'POST':
        form = MoveMoneyForm(request.POST,
                             request=request,
                             account=account,
                             cat_type=settings.TR_MOVE)
        if form.is_valid():
            cd = form.cleaned_data
            account.move_money(to_account=cd['account'],
                               amount=cd['amount'],
                               tag=cd['tag'],
                               category=cd['category'],
                               description=cd['description'])
            return redirect(reverse("accounts:details", args=[account.slug]))
    else:
        form = MoveMoneyForm(request=request, account=account, cat_type=settings.TR_MOVE)
    return render(request, "accounts/money_transfer.html", {'account': account,
                                                            'form': form,
                                                            'msg': 'Move money'})


@login_required
def exchange_money(request, slug):
    account = get_object_or_404(BankAccount, slug=slug, owner=request.user)
    #TODO: exchange logic

#endregion operations
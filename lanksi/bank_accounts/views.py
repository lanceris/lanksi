from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from .models import BankAccount, Transaction, TR_ADD, TR_MOVE, TR_WITHDRAW
from .forms import TransactionForm, MoveMoneyForm,\
                    FilterHistoryForm, BankAccountForm


def _transaction_request(request, template, account, process_method):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            process_method(amount=form.cleaned_data['amount'],
                           tag=form.cleaned_data['tag'],
                           description=form.cleaned_data['description'])
            return redirect(reverse("list_accounts"))
    else:
        form = TransactionForm()
    return render(request, template, {'form': form})


@login_required
def list_accounts(request):
    accounts = BankAccount.objects.filter(owner=request.user)
    return render(request, 'bankaccount_list.html', {'accounts': accounts})


@login_required
def add_account(request):
    if request.method == 'POST':
        form = BankAccountForm(request.POST)
        if form.is_valid():
            new_acc = form.save(commit=False)
            new_acc.owner = request.user
            new_acc.save()
            return redirect(reverse("list_accounts"))
    else:
        form = BankAccountForm()
    return render(request, 'bankaccount_add.html', {'form': form})


@login_required
def account_details(request, slug):
    account = get_object_or_404(BankAccount, slug=slug, owner=request.user)
    return render(request, "bankaccount_detail.html", {'account': account})


@login_required
def add_money(request, slug):
    account = get_object_or_404(BankAccount, slug=slug, owner=request.user)
    return _transaction_request(request, "add_money.html", account, account.add_money)


@login_required
def withdraw_money(request, slug):
    account = get_object_or_404(BankAccount, slug=slug, owner=request.user)
    return _transaction_request(request, "withdraw_money.html", account, account.withdraw_money)


@login_required
def move_money(request, slug):
    account = get_object_or_404(BankAccount, slug=slug, owner=request.user)
    if request.method == 'POST':
        form = MoveMoneyForm(request.POST, from_account=account)
        if form.is_valid():
            account.move_money(to_account=form.cleaned_data['account'],
                               amount=form.cleaned_data['amount'],
                               tag=form.cleaned_data['tag'],
                               description=form.cleaned_data['description'])
            return redirect(reverse("account-details"), args=[account.number])
    else:
        form = MoveMoneyForm(from_account=account)
    return _transaction_request(request, "move_money.html", account, account.withdraw_money)


@login_required
def history(request, slug):
    account = get_object_or_404(BankAccount, slug=slug, owner=request.user)
    from django.db.models import Q
    queryset = Transaction.objects.filter(
        Q(tr_from=account) | Q(tr_to=account)).order_by('-created')

    if request.method == 'POST':
        form = FilterHistoryForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['date_from']:
                queryset = queryset.filter(created__gte=form.cleaned_data['date_from'])
            if form.cleaned_data['date_to']:
                queryset = queryset.filter(created__lte=form.cleaned_data['date_to'])
            if form.cleaned_data['keywords']:
                queryset = queryset.filter(comment__contains=form.cleaned_data['keywords'])
    else:
        form = FilterHistoryForm()

    history_items = []
    for t in queryset:
        item = {'description': t.comment, 'datetime': t.created, 'tag': t.tr_tag,
                'debit': '', 'credit': '', 'correspondent': ''}
        if t.tr_type == TR_ADD:
            item['credit'] = t.tr_amount
            item['balance'] = t.balance
            item['balance_before'] = t.balance - t.tr_amount
        elif t.tr_type == TR_WITHDRAW:
            item['debit'] = t.tr_amount
            item['balance'] = t.balance
            item['balance_before'] = t.balance + t.tr_amount
        elif t.tr_type == TR_MOVE:
            if t.account == account:
                item['debit'] = t.tr_amount
                item['balance'] = t.balance
                item['correspondent'] = t.recipient_account
                item['balance_before'] = t.balance + t.tr_amount
            else:
                item['credit'] = t.tr_amount
                item['balance'] = t.recipient_balance
                item['correspondent'] = t.account
                item['balance_before'] = t.recipient_balance - t.tr_amount
        history_items.append(item)

    return render(request, "bankaccount_history.html", {'history': history_items, 'form': form})
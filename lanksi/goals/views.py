from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib.auth.decorators import login_required
from goals.models import Goal
from goals.forms import GoalForm, AddMoneyForm


@login_required
def list_(request):
    goals = Goal.objects.filter(owner=request.user)
    return render(request, 'goals/list_.html', {'goals': goals})


@login_required
def add(request):
    if request.method == 'POST':
        form = GoalForm(request.POST)
        if form.is_valid():
            new_cat = form.save(commit=False)
            new_cat.owner = request.user
            new_cat.save()
            return redirect(reverse("goals:list_"))
    else:
        form = GoalForm()
    return render(request, 'goals/add.html', {'form': form})


@login_required
def add_money(request, id):
    goal = get_object_or_404(Goal, id=id, owner=request.user)

    if request.method == 'POST':
        form = AddMoneyForm(request.POST, goal=goal, request=request)
        if form.is_valid():
            cd = form.cleaned_data
            goal.add_money(amount=cd['amount'],
                           acc_from=cd['acc_from'])
            return redirect(reverse("goals:list_"))
    else:
        form = AddMoneyForm(goal=goal, request=request)
    return render(request, 'goals/add_money.html', {'goal': goal,
                                                    'form': form})


@login_required
def details(request, id):
    goal = get_object_or_404(Goal, id=id, owner=request.user)
    return render(request, "goals/details.html", {'goal': goal})


@login_required
def edit(request, id):
    goal = get_object_or_404(Goal, id=id, owner=request.user)
    if request.method == 'POST':
        form = GoalForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            Goal.objects.create(owner=request.user,
                                name=cd['name'],
                                money_total=cd['money_total'],
                                money_saved=cd['money_saved'],
                                currency=cd['currency'],
                                description=cd['description'])
            goal.delete()

            return redirect(reverse("goals:list_"))
    else:
        form = GoalForm(initial={'name': goal.name,
                                 'money_total': goal.money_total,
                                 'money_saved': goal.money_saved,
                                 'currency': goal.currency,
                                 'description': goal.description})
    return render(request, "goals/edit.html", {'goal': goal,
                                               'form': form})


@login_required
def delete(request, id):
    goal = get_object_or_404(Goal, id=id, owner=request.user)
    return render(request, 'goals/delete.html', {'goal': goal})


@login_required
def confirm_delete(request, id):
    goal = get_object_or_404(Goal, id=id, owner=request.user)
    goal.delete()
    return redirect(reverse("goals:list_"))

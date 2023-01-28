from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import JsonResponse
from .models import Category, Expense
from userpreferences.models import UserPreference
import json


# Create your views here.

@login_required(login_url='/authentication/login')
def index(request):
    categories = Category.objects.all()
    expenses = Expense.objects.filter(user=request.user)
    page_number = request.GET.get('page')
    paginator = Paginator(expenses, 6)
    page_obj = Paginator.get_page(paginator, page_number)
    currency = UserPreference.objects.get(user=request.user).currency

    context = {'categories': categories, 'expenses': expenses, 'page_obj': page_obj, 'currency': currency}
    return render(request, 'expenses/index.html', context)


@login_required(login_url='/authentication/login')
def add_expense(request):
    categories = Category.objects.all()

    context = {'categories': categories, 'values': request.POST}

    if request.method == "POST":
        amount = request.POST['amount']
        description = request.POST['description']
        date = request.POST['expense_date']
        category = request.POST['category']

        if not amount:
            messages.error(request, 'Amount is required')
            return render(request, 'expenses/add_expense.html', context)

        if not description:
            messages.error(request, 'Description is required')
            return render(request, 'expenses/add_expense.html', context)

        Expense.objects.create(
            user=request.user,
            amount=amount,
            description=description,
            date=date,
            category=category,
        )

        messages.success(request, 'Expense added successfully')
        return redirect('expenses')

    return render(request, 'expenses/add_expense.html', context)


@login_required(login_url='/authentication/login')
def update_expense(request, id):
    expense = Expense.objects.get(pk=id)
    categories = Category.objects.all()
    context = {'expense': expense, 'values': expense, 'categories': categories}

    if request.method == 'GET':
        return render(request, 'expenses/update_expense.html', context)

    if request.method == 'POST':
        amount = request.POST['amount']
        description = request.POST['description']
        date = request.POST['expense_date']
        category = request.POST['category']

        if not amount:
            messages.error(request, 'Amount is required')
            return render(request, 'expenses/update_expense.html', context)

        if not description:
            messages.error(request, 'Description is required')
            return render(request, 'expenses/update_expense.html', context)

        expense.owner = request.user
        expense.amount = amount
        expense.description = description
        expense.date = date
        expense.category = category
        expense.save()

        messages.success(request, "Expense updated successfully")
        return redirect('expenses')


@login_required(login_url='/authentication/login')
def delete_expense(request, id):
    expense = Expense.objects.get(pk=id, user=request.user)
    expense.delete()

    messages.success(request, "Expense deleted successfully")
    return redirect("expenses")


@login_required(login_url='/authentication/login')
def search_expenses(request):
    if request.method == "POST":
        search_string = json.loads(request.body).get("searchText")

        expenses = Expense.objects.filter(
            user=request.user,
            amount__istartswith=search_string
        ) | Expense.objects.filter(
            user=request.user,
            date__istartswith=search_string
        ) | Expense.objects.filter(
            user=request.user,
            description__icontains=search_string
        ) | Expense.objects.filter(
            user=request.user,
            category__icontains=search_string
        )

        data = expenses.values()

        return JsonResponse(list(data), safe=False)




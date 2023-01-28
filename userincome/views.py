from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .models import Income, Source
from django.http import JsonResponse
from userpreferences.models import UserPreference
import json


# Create your views here.
@login_required(login_url='/authentication/login')
def index(request):
    sources = Source.objects.all()
    incomes = Income.objects.filter(user=request.user)
    page_number = request.GET.get('page')
    paginator = Paginator(incomes, 6)
    page_obj = Paginator.get_page(paginator, page_number)
    currency = UserPreference.objects.get(user=request.user).currency

    context = {'sources': sources, 'income': incomes, 'page_obj': page_obj, 'currency': currency}
    return render(request, 'income/index.html', context)


@login_required(login_url='/authentication/login')
def add_income(request):
    sources = Source.objects.all()

    context = {'sources': sources, 'values': request.POST}

    if request.method == "POST":
        amount = request.POST['amount']
        description = request.POST['description']
        date = request.POST['income_date']
        source = request.POST['source']

        if not amount:
            messages.error(request, 'Amount is required')
            return render(request, 'income/add_income.html', context)

        if not description:
            messages.error(request, 'Description is required')
            return render(request, 'income/add_income.html', context)

        Income.objects.create(
            user=request.user,
            amount=amount,
            description=description,
            date=date,
            source=source,
        )

        messages.success(request, 'Income record added successfully')
        return redirect('income')

    return render(request, 'income/add_income.html', context)


@login_required(login_url='/authentication/login')
def update_income(request, id):
    income = Income.objects.get(pk=id)
    sources = Source.objects.all()
    context = {'income': income, 'values': income, 'sources': sources}

    if request.method == 'GET':
        return render(request, 'income/update_income.html', context)

    if request.method == 'POST':
        amount = request.POST['amount']
        description = request.POST['description']
        date = request.POST['income_date']
        source = request.POST['source']

        if not amount:
            messages.error(request, 'Amount is required')
            return render(request, 'income/update_income.html', context)

        if not description:
            messages.error(request, 'Description is required')
            return render(request, 'income/update_income.html', context)

        income.owner = request.user
        income.amount = amount
        income.description = description
        income.date = date
        income.category = source
        income.save()

        messages.success(request, "Income updated successfully")
        return redirect('income')


@login_required(login_url='/authentication/login')
def delete_income(request, id):
    income = Income.objects.get(pk=id, user=request.user)
    income.delete()

    messages.success(request, "Income deleted successfully")
    return redirect("income")


@login_required(login_url='/authentication/login')
def search_income(request):
    if request.method == "POST":
        search_string = json.loads(request.body).get("searchText")

        incomes = Income.objects.filter(
            user=request.user,
            amount__istartswith=search_string
        ) | Income.objects.filter(
            user=request.user,
            date__istartswith=search_string
        ) | Income.objects.filter(
            user=request.user,
            description__icontains=search_string
        ) | Income.objects.filter(
            user=request.user,
            source__icontains=search_string
        )

        data = incomes.values()

        return JsonResponse(list(data), safe=False)

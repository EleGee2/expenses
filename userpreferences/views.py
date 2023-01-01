import json
import os

from django.conf import settings
from django.contrib import messages
from django.shortcuts import render

from .models import UserPreference


# Create your views here.

def index(request):
    currency_data = []
    user_preferences = None
    file_path = os.path.join(settings.BASE_DIR, 'currencies.json')

    with open(file_path, 'r') as json_file:
        data = json.load(json_file)

        for k, v in data.items():
            currency_data.append({'name': k, 'value': v})

    if request.method == 'GET':
        user_preferences = UserPreference.objects.get(user=request.user)
        return render(request, 'preferences/index.html', {'currencies': currency_data,
                                                          'user_preferences': user_preferences
                                                          })
    else:
        exists = UserPreference.objects.filter(user=request.user).exists()
        currency = request.POST['currency']
        if exists:
            user_preferences = UserPreference.objects.get(user=request.user)
            user_preferences.currency = currency
            user_preferences.save()
            messages.success(request, 'Changes saved successfully')
        else:
            user_preferences = UserPreference.objects.create(user=request.user, currency=currency)
            messages.success(request, 'Currency saved successfully')

        return render(request, 'preferences/index.html', {'currencies': currency_data,
                                                          'user_preferences': user_preferences
                                                          })





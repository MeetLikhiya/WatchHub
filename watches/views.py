from urllib import request
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from .models import Watch

# Create your views here.

def home(request):
    return render(request, 'watches/home.html')

def all_categories(request):
    watches = Watch.objects.all()
    return render(request, 'watches/category.html', {
        'watches': watches,
        'category': 'All Watches'
    })
 

class CategoryView(View):
    def get(self, request, category):
        watches = Watch.objects.filter(category=category)
        return render(request, 'watches/category.html', {'watches': watches, 'category': category}) 

from django.shortcuts import render
from django.http import HttpResponse

def viewFunct(request):
    # Pull data
    return HttpResponse('Test')


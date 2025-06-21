from django.shortcuts import render
from django.http import JsonResponse


def hello_world(request):
    return render(request, "base.html")


def api_hello(request):
    return JsonResponse({"message": "Hello World from Django!"})

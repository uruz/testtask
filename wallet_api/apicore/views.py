from django.shortcuts import render
from django.http import HttpResponse

def ping(HttpRequest):
    return HttpResponse(content='200 OK!', status=200)

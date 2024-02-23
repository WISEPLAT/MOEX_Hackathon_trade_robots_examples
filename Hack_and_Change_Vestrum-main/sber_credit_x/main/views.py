from django.shortcuts import render

def index(request):
    return render(request, 'main/index.html')


def workspace(request):
    return render(request, 'main/workspace.html')


def workspace1(request):
    return render(request, 'main/workspace1.html')


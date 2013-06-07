from django.shortcuts import render

def overview(request):
    return render(request, "docs/base.html")
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse

from .models import CtaUser

def signup(request):
    try:
        cta = CtaUser(email=request.POST['email'])
        cta.save()
    except Exception,e:
        return render(request, 'cta/detail.html', {
            'error_message': "That email is already registered.",
        })
    else:
        return render(request, 'cta/results.html', {})


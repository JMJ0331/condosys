from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from incidents.forms import IncidentForm
from payments.forms import PaymentForm
from visitors.forms import VisitorForm

# Create your views here.

def inicio(request):
    contexto = {
        'payment_form': PaymentForm(),
        'visitor_form': VisitorForm(),
        'incident_form': IncidentForm(),
    }
    return render(request, 'inicio/index.html', contexto)
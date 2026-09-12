from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.views.generic import ListView

from incidents.forms import IncidentForm
from payments.forms import PaymentForm
from residents.models import Resident
from structure.models import Apartment, Building, Garden
from visitors.forms import VisitorForm


class InicioView(ListView):
    template_name = 'inicio/index.html'
    context_object_name = 'residentes'
    model = Resident
    paginate_by = 12

    def get_queryset(self):
        qs = Resident.objects.select_related(
            'user',
            'apartment__building__garden',
        ).all()

        search = self.request.GET.get('search', '').strip()
        garden = self.request.GET.get('garden', '')
        building = self.request.GET.get('building', '')
        apartment = self.request.GET.get('apartment', '')

        if search:
            qs = qs.filter(
                Q(full_name__icontains=search)
                | Q(cedula__icontains=search)
                | Q(email__icontains=search)
                | Q(user__first_name__icontains=search)
                | Q(user__last_name__icontains=search)
                | Q(user__email__icontains=search)
            )
        if garden:
            qs = qs.filter(apartment__building__garden_id=garden)
        if building:
            qs = qs.filter(apartment__building_id=building)
        if apartment:
            qs = qs.filter(apartment_id=apartment)

        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['payment_form'] = PaymentForm()
        ctx['visitor_form'] = VisitorForm()
        ctx['incident_form'] = IncidentForm()
        ctx['residentes_pago'] = Resident.objects.select_related('apartment').all()
        ctx['jardines'] = Garden.objects.filter(is_active=True)
        ctx['edificios'] = Building.objects.filter(is_active=True)
        ctx['departamentos'] = Apartment.objects.filter(is_active=True)
        ctx['search_actual'] = self.request.GET.get('search', '')
        ctx['garden_actual'] = self.request.GET.get('garden', '')
        ctx['building_actual'] = self.request.GET.get('building', '')
        ctx['apartment_actual'] = self.request.GET.get('apartment', '')
        return ctx

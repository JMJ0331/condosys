from django.db.models import Q
from django.views.generic import ListView

from payments.models import Payment
from residents.models import Resident
from structure.models import Apartment, Building, Garden
from visitors.models import Visitor


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
        ctx['jardines'] = Garden.objects.filter(is_active=True)
        ctx['edificios'] = Building.objects.filter(is_active=True)
        ctx['departamentos'] = Apartment.objects.filter(is_active=True)
        ctx['search_actual'] = self.request.GET.get('search', '')
        ctx['garden_actual'] = self.request.GET.get('garden', '')
        ctx['building_actual'] = self.request.GET.get('building', '')
        ctx['apartment_actual'] = self.request.GET.get('apartment', '')
        ctx['total_departamentos'] = Apartment.objects.filter(is_active=True).count()
        ctx['total_residentes'] = Resident.objects.filter(is_active=True).count()
        ctx['total_pagos'] = Payment.objects.count()
        ctx['total_visitantes'] = Visitor.objects.count()
        return ctx

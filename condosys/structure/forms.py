from django import forms
from .models import Apartment, Building, Garden


class GardenForm(forms.ModelForm):
    class Meta:
        model = Garden
        fields = ['name', 'location', 'description', 'is_active']


class BuildingForm(forms.ModelForm):
    class Meta:
        model = Building
        fields = [
            'garden', 'name', 'number_of_floors', 'description', 'is_active',
        ]


class ApartmentsForm(forms.ModelForm):
    class Meta:
        model = Apartment
        fields = [
            'building', 'number', 'floor', 'area_m2', 'type', 'status',
            'is_active',
        ]

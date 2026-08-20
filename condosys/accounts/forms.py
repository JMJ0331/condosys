from django import forms
from .models import User


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'email', 'first_name', 'last_name', 'phone', 'document',
            'avatar_url', 'role', 'status', 'garden_id', 'is_active',
        ]


class UserCreateForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, min_length=8)
    password_confirmation = forms.CharField(widget=forms.PasswordInput, min_length=8)

    class Meta:
        model = User
        fields = [
            'email', 'first_name', 'last_name', 'phone', 'document',
            'avatar_url', 'role', 'status', 'garden_id', 'is_active',
        ]

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirmation = cleaned_data.get('password_confirmation')
        if password and confirmation and password != confirmation:
            self.add_error('password_confirmation', 'Las contraseñas no coinciden.')
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user

from django import forms
from django.core.exceptions import ValidationError

from .models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['table_number', 'status', 'items']
        widgets = {
            'items': forms.CheckboxSelectMultiple,
        }

    def clean_table_number(self):
        table_number = self.cleaned_data.get('table_number')

        if table_number <= 0:
            raise ValidationError(
                'Номер стола должен быть положительным целым числом.'
            )

        return table_number

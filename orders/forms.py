from django import forms
from .models import Order


class OrderForm(forms.ModelForm):

    class Meta:
        model = Order
        fields = ('title', 'description', 'word_count', 'deadline')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
        self.fields['deadline'].widget = forms.DateInput(
            attrs={'class': 'form-control', 'type': 'date'}
        )
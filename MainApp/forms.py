from Management.models import Orders
from django import forms


class Orderform(forms.ModelForm):
    OrderedBy=forms.CharField(max_length=120)
    Item = forms.CharField(max_length=120)
    class Meta:
        model = Orders
        fields=["OrderedBy","Item"]

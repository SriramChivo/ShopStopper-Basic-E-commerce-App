from django import forms
from .models import Orders, Products, Tags, Customer
from django.core.validators import RegexValidator
from django.contrib.admin.widgets import FilteredSelectMultiple


class Editform(forms.ModelForm):

    class Meta:
        model = Orders
        exclude = []

    def __init__(self, *args, **kwargs):
        super(Editform, self).__init__(*args, **kwargs)
        # to remove the empty dashes from the dropdown filed when usinf foreign keys fields
        self.fields['OrderedBy'].empty_label = None
        self.fields['Item'].empty_label = None
        self.fields['Status'].empty_label = None
        # following line needed to refresh widget copy of choice list
        self.fields['Status'].widget.choices = self.fields['Status'].choices
        self.fields['OrderedBy'].queryset = Customer.objects.all()
        self.fields['Item'].queryset = Products.objects.all()


class AddProd(forms.ModelForm):

    Catgory = (
        ('Indoor', 'Indoor'),
        ('OutDoor', 'OutDoor')
    )

    Productname = forms.CharField(label="Name Of the Product", max_length=60, validators=[
                                  RegexValidator(r'^[A-Za-z0-9 ]*$', "Only Alphabets and numericals allowed")],
                                  widget=forms.TextInput(attrs={"Placeholder": "product Name", "class": "form-control mb-3 mt-1", "size": "10"}))
    Category = forms.ChoiceField(choices=Catgory,
                                 widget=forms.RadioSelect(attrs={"class": "form-check-input"}))
    description = forms.CharField(label="Description", max_length=60, validators=[RegexValidator(r'^[A-Za-z0-9 ]*$', "Only Alphabets and numericals allowed")],
                                  widget=forms.Textarea(attrs={"Placeholder": "Description", "class": "form-control mb-3 mt-1", "cols": "30", "rows": "5"}))
    Price = forms.IntegerField(label="Price", validators=[
        RegexValidator(r'^[0-9]*$', "Only numericals allowed")],
        widget=forms.NumberInput(attrs={"Placeholder": "Price", "class": "form-control mb-3 mt-1"}))
    Tags = forms.ModelMultipleChoiceField(queryset=Tags.objects.all(),
                                          widget=forms.CheckboxSelectMultiple(attrs={"class": "form-check-input"}))

    class Meta:
        model = Products
        fields = "__all__"

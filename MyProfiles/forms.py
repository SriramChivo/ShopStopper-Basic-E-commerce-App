from Management.models import Tags, Products, Orders, Customer, State
from django.core.validators import RegexValidator
from django import forms

choices = [tuple([i, i]) for i in State.objects.all()]


class customerProfile(forms.ModelForm):
    # Profile = forms.CharField(label="PrimaryUser", max_length=60,
    #                           widget=forms.TextInput(attrs={"readonly": "readonly"}))

    Phone = forms.CharField(label="Phone", validators=[
        RegexValidator(
            r"^[0-9]*$", "It can be only numericals")],
        widget=forms.TextInput(attrs={"placeholder": "Phone"}))
    State = forms.CharField(widget=forms.Select(choices=choices))

    class Meta:
        model = Customer
        fields = "__all__"
        exclude = ["Profile"]

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields["State"].choices = State.objects.all()

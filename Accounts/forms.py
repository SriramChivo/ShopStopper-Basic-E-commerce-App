from .models import Accounts
from django import forms
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError

# i am creating model form because of i need to save the user input to the models

validator_fn = [
    RegexValidator(r'^[0-9]*$',
                   "Use atleast one alphabets and SpeciaCharacters", "invalid", True),
    RegexValidator(r'^[A-Za-z]*$',
                   "Use atleast one numericals and SpeciaCharacters", "invalid", True),
    RegexValidator(r'^[!@#$%^&*]*$',
                   "Use atleast one numericals and Alphabets", "invalid", True)]


def regex_validators(value):
    err = None
    cont = 0
    for validator in validator_fn:
        try:
            print("value")
            l = validator(value)
            print(l)
            cont += 1
            if cont == 3:
                return value
            # Valid value, return it
        except ValidationError as exc:
            print(value)
            err = exc
            print(err)
    # Value match nothing, raise error
    raise err


class AccountsForm(forms.ModelForm):

    Email = forms.EmailField(label="Email-Address", max_length=60,
                             min_length=8, help_text="Please Provide Valid EmailAddress",
                             widget=forms.EmailInput(attrs={'placeholder': 'Enter a Email', 'size': '20', 'class': 'form-control'}))
    UserName = forms.CharField(label="Username", max_length=60,
                               min_length=3, help_text="Please Provide Valid Username",
                               widget=forms.TextInput(attrs={'placeholder': 'Enter a Username', 'size': '20', 'class': 'form-control'}))
    password1 = forms.CharField(label="Password", min_length=6, validators=[regex_validators],
                                widget=forms.PasswordInput(
                                    attrs={'placeholder': 'Password', 'class': 'form-control'}))
    password2 = forms.CharField(label="Confirm Password",
                                widget=forms.PasswordInput(
                                    attrs={'placeholder': 'Confirm Password', 'class': 'form-control'}))

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        Accounts = super().save(commit=False)
        Accounts.set_password(self.cleaned_data["password1"])
        if commit:
            Accounts.save()
        return Accounts

    class Meta:
        model = Accounts
        fields = ['Email', 'UserName']


class loginForm(forms.Form):
    Email = forms.CharField(label="Email", max_length=60, required=True, widget=forms.EmailInput(
        attrs={'placeholder': 'Enter a Email', 'size': '20', 'class': 'form-control'}))
    password = forms.CharField(label="Password",
                               widget=forms.PasswordInput(
                                   attrs={'placeholder': 'Password', 'class': 'form-control'}))

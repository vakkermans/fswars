from django import forms

class PickNameForm(forms.Form):
    name         = forms.CharField(max_length=15)

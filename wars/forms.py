from django import forms

class PickNameForm(forms.Form):
    message         = forms.CharField(max_length=15)

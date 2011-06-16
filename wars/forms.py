from django import forms

class PickNameForm(forms.Form):
    nickname         = forms.CharField(max_length=15)

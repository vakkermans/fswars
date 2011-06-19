from django import forms

class PickNameForm(forms.Form):
    nickname         = forms.CharField(max_length=15)

class PickSoundsForm(forms.Form):
    sound_ids        = forms.CharField(max_length=1024)

class UpdateBattleForm(forms.Form):
    message          = forms.CharField(max_length=2048)

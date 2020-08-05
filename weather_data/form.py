from django import forms

# django 中的 Form类
class RegionForm(forms.Form):
    latitude = forms.FloatField()
    longtitude = forms.FloatField()
    is_display = forms.BooleanField(required=False)
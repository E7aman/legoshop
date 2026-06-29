from django import forms

QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 21)]


class AddToCartForm(forms.Form):
    quantity = forms.TypedChoiceField(choices=QUANTITY_CHOICES, coerce=int)
    override = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)

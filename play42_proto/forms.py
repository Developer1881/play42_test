from django import forms

from .models import Bet, DoubleBet, TripleBet, NBet

class BetForm(forms.ModelForm):

    class Meta:
        model = Bet
        fields = ('probability', 'sum',)


class DoubleBetForm(forms.ModelForm):

    class Meta:
        model = DoubleBet
        fields = ('probability1', 'sum1', 'probability2', 'sum2',)

        def __init__(self, data=None, files=None, request=None, recipient_list=None, *args, **kwargs):
            super().__init__(data=data, files=files, request=request, recipient_list=recipient_list,
                             *args, **kwargs)
            self.fields['probability1'].widget.attrs['placeholder'] = 'Вероятность1'
            self.fields['sum1'].widget.attrs['placeholder'] = 'Ставка1'


class TripleBetForm(forms.ModelForm):

    class Meta:
        model = TripleBet
        fields = ('probability1', 'sum1', 'probability2', 'sum2', 'probability3', 'sum3',)

class NBetForm(forms.ModelForm):

    class Meta:
        model = NBet
        fields = ('n_players',)


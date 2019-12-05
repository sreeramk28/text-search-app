from django import forms

class TextForm(forms.Form):
    doctext = forms.CharField(widget=forms.Textarea(attrs={'rows':29, 'cols':79}), label='Document Text')
    #word = forms.CharField()
class SearchForm(forms.Form):
    word = forms.CharField(required = False)
#attrs={'rows':x, 'cols':y}

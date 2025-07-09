from django import forms

class SentenceCompletionForm(forms.Form):
    partial_sentence = forms.CharField(
        label="Andian-teny tsy feno hamenoana",
        max_length=500,
        widget=forms.Textarea(attrs={'rows': 4, 'cols': 50})
    )
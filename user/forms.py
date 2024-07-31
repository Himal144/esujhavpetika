from django import forms

class SuggestionForm(forms.Form):
    name = forms.CharField(max_length=100, required=False,widget=forms.TextInput(attrs={'class':'form-control',id:"modal-name", 'placeholder':'Name'}))
    email = forms.EmailField(required=False,widget=forms.EmailInput(attrs={'class':'form-control','placeholder':'Email'}))
    topic = forms.CharField(max_length=100, required=True,widget=forms.TextInput(attrs={'class':'form-control', 'id':'suggestionTopic',}))
    suggestion = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','id':'suggestion'}), required=True,)
    fields=['name','email','topic','suggestion']

    def __init__(self, *args, **kwargs):
        authenticated_sender = kwargs.pop('authenticated_sender', False)
        super(SuggestionForm, self).__init__(*args, **kwargs)
        
        if not authenticated_sender:
            self.fields['name'].widget = forms.HiddenInput()

           
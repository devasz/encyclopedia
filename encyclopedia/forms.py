from django import forms


class NewEntryForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(NewEntryForm, self).__init__(*args, **kwargs)

        for k, field in self.fields.items():
            if 'required' in field.error_messages:
                field.error_messages['required'] = 'This field is required'

    title = forms.CharField(label='',
                            widget=forms.TextInput(attrs={'class': 'form-control',
                                                          'placeholder': "Enter a title for the page"}), required=True)
    content = forms.CharField(label='',
                              widget=forms.Textarea(attrs={'class': 'form-control',
                                                           'placeholder': "Enter the Markdown content for the page"}),
                              required=True)


class EditEntryForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(EditEntryForm, self).__init__(*args, **kwargs)

        for k, field in self.fields.items():
            if 'required' in field.error_messages:
                field.error_messages['required'] = 'This field is required'

    title = forms.CharField(label='', initial='title',
                            widget=forms.TextInput(attrs={'class': 'form-control'}), required=True)
    content = forms.CharField(label='', initial='content',
                              widget=forms.Textarea(attrs={'class': 'form-control'}), required=True)

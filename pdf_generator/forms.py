from django import forms
from .models import PDFTemplate

class PDFTemplateForm(forms.ModelForm):
    class Meta:
        model = PDFTemplate
        fields = ['name', 'template_file']

class CSVUploadForm(forms.Form):
    csv_file = forms.FileField()
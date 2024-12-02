from django.shortcuts import render, redirect
from django.urls import reverse
from django.conf import settings
import os
from .models import PDFTemplate, GeneratedPDF
from .forms import PDFTemplateForm, CSVUploadForm
from .utils import WyomingLLCDissolutionForm

def upload_template(request):
    if request.method == 'POST':
        form = PDFTemplateForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('template_list')
    else:
        form = PDFTemplateForm()
    return render(request, 'pdf_generator/upload_template.html', {'form': form})

def template_list(request):
    templates = PDFTemplate.objects.all()
    return render(request, 'pdf_generator/template_list.html', {'templates': templates})

def generate_pdf(request, template_id):
    template = PDFTemplate.objects.get(id=template_id)
    
    if request.method == 'POST':
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['csv_file']
            csv_data = csv_file.read()
            
            # Process the PDF using the Wyoming LLC form processor
            output_paths = WyomingLLCDissolutionForm.process_pdf(
                template.template_file.path, 
                csv_data
            )
            
            # Save generated PDFs
            for path in output_paths:
                relative_path = os.path.relpath(path, settings.MEDIA_ROOT)
                GeneratedPDF.objects.create(
                    template=template,
                    output_file=relative_path
                )
            
            return redirect('generated_pdf_list')
    else:
        form = CSVUploadForm()
    
    return render(request, 'pdf_generator/generate_pdf.html', {
        'form': form,
        'template': template
    })

def generated_pdf_list(request):
    pdfs = GeneratedPDF.objects.all().order_by('-generated_at')
    return render(request, 'pdf_generator/generated_pdf_list.html', {'pdfs': pdfs})
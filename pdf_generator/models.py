from django.db import models

class PDFTemplate(models.Model):
    name = models.CharField(max_length=100)
    template_file = models.FileField(upload_to='pdf_templates/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class GeneratedPDF(models.Model):
    template = models.ForeignKey(PDFTemplate, on_delete=models.CASCADE)
    output_file = models.FileField(upload_to='generated_pdfs/')
    generated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Generated PDF from {self.template.name} at {self.generated_at}"
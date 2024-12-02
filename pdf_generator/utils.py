# pdf_generator/utils.py
import csv
import io
import os
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch

class WyomingLLCDissolutionForm:
    # Field positions with your provided coordinates
    FIELD_POSITIONS = {
        'company_name': (100, 550),     # Company name field after "1. The name of the limited liability company is:"
        'date': (430, 405),             # Date field
        'print_name': (100, 360),       # Print Name field
        'contact_person': (430, 360),    # Contact Person field
        'title': (100, 330),            # Title field
        'phone': (450, 330),            # Phone Number field
        'email': (350, 305),            # Email field
    }
    
    @staticmethod
    def process_pdf(template_path, csv_data):
        # Read CSV data
        csv_file = io.StringIO(csv_data.decode('utf-8'))
        csv_reader = csv.DictReader(csv_file)
        
        output_pdfs = []
        
        for row in csv_reader:
            # Create a new PDF with reportlab
            packet = io.BytesIO()
            c = canvas.Canvas(packet, pagesize=letter)
            
            # In utils.py, modify the safe_filename generation:
            company_name = row.get('The name of the limited liability company is', 'output')
            # Replace special characters (like ■) with a space
            company_name = company_name.replace('■', ' ')
            # Then create safe filename
            safe_filename = "".join(x for x in company_name if x.isalnum() or x in (' ', '-', '_', ',', '.')).strip()
            
            # Add company name with larger font
            c.setFont("Helvetica-Bold", 13)  # Larger font for company name and bold
            c.drawString(
                WyomingLLCDissolutionForm.FIELD_POSITIONS['company_name'][0],
                WyomingLLCDissolutionForm.FIELD_POSITIONS['company_name'][1],
                company_name
            )
            
            # Reset font size for other fields
            c.setFont("Helvetica", 11)
            
            # Add text fields with precise positioning
            field_mappings = {
                'date': 'Date',
                'print_name': 'Print Name',
                'contact_person': 'Contact Person',
                'title': 'Title',
                'phone': 'Daytime Phone Number',
                'email': 'Email'
            }
            
            for field, csv_key in field_mappings.items():
                if field in WyomingLLCDissolutionForm.FIELD_POSITIONS:
                    value = row.get(csv_key, '')
                    x = WyomingLLCDissolutionForm.FIELD_POSITIONS[field][0]
                    y = WyomingLLCDissolutionForm.FIELD_POSITIONS[field][1]
                    c.drawString(x, y, value)
            
            c.save()
            
            # Move to the beginning of the BytesIO buffer
            packet.seek(0)
            new_pdf = PdfReader(packet)
            
            # Read the existing PDF
            existing_pdf = PdfReader(open(template_path, "rb"))
            output = PdfWriter()
            
            # Add the "watermark" (new pdf) on the existing page
            page = existing_pdf.pages[0]
            page.merge_page(new_pdf.pages[0])
            output.add_page(page)
            
            # Create output filename using company name
            output_path = f"media/generated_pdfs/{safe_filename}.pdf"
            
            # Ensure unique filename if file exists
            counter = 1
            base_path = output_path[:-4]
            while os.path.exists(output_path):
                output_path = f"{base_path}_{counter}.pdf"
                counter += 1
            
            with open(output_path, "wb") as outputStream:
                output.write(outputStream)
            
            output_pdfs.append(output_path)
        
        return output_pdfs
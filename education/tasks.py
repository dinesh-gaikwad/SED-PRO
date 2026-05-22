  
from celery import shared_task
from django.contrib.auth import get_user_model
from django.core.mail import EmailMessage
from django.conf import settings
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from io import BytesIO
from datetime import datetime

User = get_user_model()

@shared_task
def generate_certificate_task(user_id, level):
    try:
        user = User.objects.get(id=user_id)
        
        buffer = BytesIO()
        p = canvas.Canvas(buffer, pagesize=A4)
        width, height = A4
        
        p.setFont('Helvetica-Bold', 24)
        p.drawCentredString(width/2, height-150, 'EntreSkill Hub')
        
        p.setFont('Helvetica-Bold', 20)
        p.drawCentredString(width/2, height-200, 'Certificate of Completion')
        
        p.setFont('Helvetica', 16)
        p.drawCentredString(width/2, height-280, 'This is to certify that')
        
        p.setFont('Helvetica-Bold', 18)
        p.drawCentredString(width/2, height-320, user.get_full_name() or user.email)
        
        p.setFont('Helvetica', 16)
        p.drawCentredString(width/2, height-380, f'has successfully completed the {level} course')
        
        p.drawCentredString(width/2, height-420, f'with a score of {getattr(user, f"{level}_percentage"):.1f} percent')
        
        p.setFont('Helvetica', 12)
        p.drawCentredString(width/2, height-500, f'Date: {datetime.now().strftime("%B %d, %Y")}')
        
        p.showPage()
        p.save()
        
        buffer.seek(0)
        pdf_content = buffer.getvalue()
        buffer.close()
        
        filename = f'{level}_certificate_{user.id}.pdf'
        
        if level == '10th':
            user.tenth_certificate.save(filename, BytesIO(pdf_content), save=True)
        elif level == '12th':
            user.twelfth_certificate.save(filename, BytesIO(pdf_content), save=True)
        elif level == 'graduation':
            user.graduation_certificate.save(filename, BytesIO(pdf_content), save=True)
        
        email = EmailMessage(
            subject=f'Your {level} Course Certificate - EntreSkill Hub',
            body=f'Congratulations {user.first_name}! You have passed the {level} course with {getattr(user, f"{level}_percentage"):.1f} percent. Please find your certificate attached.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[user.email],
        )
        email.attach(filename, pdf_content, 'application/pdf')
        email.send()
        
        return f'Certificate generated and sent to {user.email}'
    except Exception as e:
        return f'Error: {str(e)}'
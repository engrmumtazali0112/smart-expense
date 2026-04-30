from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.enums import TA_RIGHT, TA_CENTER
import io

def generate_invoice_pdf(invoice) -> bytes:
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=20*mm, leftMargin=20*mm,
                            topMargin=20*mm, bottomMargin=20*mm)
    styles = getSampleStyleSheet()
    story = []

    # Header
    title_style = ParagraphStyle('Title', parent=styles['Heading1'],
                                  fontSize=28, textColor=colors.HexColor('#6d28d9'),
                                  spaceAfter=2*mm)
    story.append(Paragraph("INVOICE", title_style))

    # Invoice meta
    meta_style = ParagraphStyle('Meta', parent=styles['Normal'], fontSize=10, spaceAfter=1*mm)
    story.append(Paragraph(f"<b>Invoice #:</b> {invoice.invoice_number}", meta_style))
    story.append(Paragraph(f"<b>Date:</b> {invoice.created_at.strftime('%B %d, %Y')}", meta_style))
    if invoice.due_date:
        story.append(Paragraph(f"<b>Due Date:</b> {invoice.due_date.strftime('%B %d, %Y')}", meta_style))
    story.append(Paragraph(f"<b>Status:</b> {invoice.status.value.upper()}", meta_style))
    story.append(Spacer(1, 5*mm))

    # Client
    story.append(Paragraph("<b>Bill To:</b>", meta_style))
    story.append(Paragraph(invoice.client_name, meta_style))
    if invoice.client_email:
        story.append(Paragraph(invoice.client_email, meta_style))
    story.append(Spacer(1, 8*mm))

    # Items table
    data = [["Description", "Qty", "Unit Price", "Subtotal"]]
    for item in invoice.items:
        data.append([
            item.description,
            str(item.quantity),
            f"${item.unit_price:,.2f}",
            f"${item.subtotal:,.2f}"
        ])

    # Total row
    data.append(["", "", "TOTAL", f"${invoice.total:,.2f}"])

    table = Table(data, colWidths=[90*mm, 20*mm, 35*mm, 35*mm])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#6d28d9')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('ALIGN', (1, 0), (-1, -1), 'RIGHT'),
        ('ROWBACKGROUNDS', (0, 1), (-1, -2), [colors.white, colors.HexColor('#f5f3ff')]),
        ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
        ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#ede9fe')),
        ('LINEBELOW', (0, 0), (-1, 0), 1, colors.HexColor('#6d28d9')),
        ('LINEABOVE', (0, -1), (-1, -1), 1, colors.HexColor('#6d28d9')),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(table)

    if invoice.notes:
        story.append(Spacer(1, 8*mm))
        story.append(Paragraph(f"<b>Notes:</b> {invoice.notes}", meta_style))

    doc.build(story)
    return buffer.getvalue()

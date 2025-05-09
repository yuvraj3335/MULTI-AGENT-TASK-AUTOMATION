from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import logging

logger = logging.getLogger(__name__)

class BRDAuthorAgent:
    def generate_brd(self, selected_key_points):
        logger.info("Generating BRD content")
        content = "# Business Requirement Document\n\n"
        content += "## Objective\nTo address key insights from the input.\n\n"
        content += "## Requirements\n" + "\n".join(f"- {point}" for point in selected_key_points) + "\n\n"
        content += "## Scope\nCovers the listed requirements.\n"
        logger.info("BRD content generated")
        return content

    def generate_pdf(self, content, pdf_path):
        logger.info(f"Generating PDF at {pdf_path}")
        c = canvas.Canvas(pdf_path, pagesize=letter)
        y = 750
        for line in content.split('\n'):
            if line.startswith('# '):
                c.setFont("Helvetica-Bold", 16)
                c.drawString(100, y, line[2:])
                y -= 30
            elif line.startswith('## '):
                c.setFont("Helvetica-Bold", 14)
                c.drawString(100, y, line[3:])
                y -= 20
            elif line.startswith('- '):
                c.setFont("Helvetica", 12)
                c.drawString(120, y, line[2:])
                y -= 15
            else:
                c.setFont("Helvetica", 12)
                c.drawString(100, y, line)
                y -= 15
            if y < 50:
                c.showPage()
                y = 750
        c.save()
        logger.info(f"PDF generated at {pdf_path}")
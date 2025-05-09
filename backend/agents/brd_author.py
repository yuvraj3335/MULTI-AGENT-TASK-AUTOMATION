from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from datetime import datetime
import logging
import re

logger = logging.getLogger(__name__)

class BRDAuthorAgent:
    def _categorize_points(self, points):
        """Categorize key points into different sections based on content analysis"""
        categories = {
            'prerequisites': [],
            'setup': [],
            'security': [],
            'access': [],
            'configuration': [],
            'other': []
        }
        
        for point in points:
            text = point.lower()
            if any(word in text for word in ['require', 'prerequisite', 'need', 'must have']):
                categories['prerequisites'].append(point)
            elif any(word in text for word in ['setup', 'install', 'configure', 'deployment']):
                categories['setup'].append(point)
            elif any(word in text for word in ['security', 'password', 'credential', 'vpn', 'authentication']):
                categories['security'].append(point)
            elif any(word in text for word in ['access', 'login', 'rdp', 'connect']):
                categories['access'].append(point)
            elif any(word in text for word in ['config', 'setting', 'parameter', 'option']):
                categories['configuration'].append(point)
            else:
                categories['other'].append(point)
        
        return {k: v for k, v in categories.items() if v}  # Remove empty categories

    def _format_point(self, point):
        """Format a key point into a more readable form"""
        # Remove extra spaces and normalize
        point = re.sub(r'\s+', ' ', point).strip()
        # Ensure proper sentence capitalization
        if point and not point.endswith(('.', '!', '?')):
            point += '.'
        return point[0].upper() + point[1:]

    def generate_brd(self, selected_key_points):
        logger.info("Generating BRD content")
        
        # Categorize and format key points
        formatted_points = [self._format_point(point) for point in selected_key_points]
        categories = self._categorize_points(formatted_points)
        
        # Generate BRD content with proper structure
        content = f"""# Business Requirements Document

## Document Information
- Date: {datetime.now().strftime('%Y-%m-%d')}
- Version: 1.0
- Status: Draft

## Executive Summary
This document outlines the business requirements for the system implementation based on the analyzed inputs.

## Objective
To provide a comprehensive guide for system implementation while ensuring security, accessibility, and proper configuration.

## Scope
This document covers the requirements, procedures, and configurations needed for successful system implementation.

## Detailed Requirements

"""
        # Add categorized requirements
        for category, points in categories.items():
            if points:
                content += f"### {category.title()}\n"
                for i, point in enumerate(points, 1):
                    content += f"{i}. {point}\n"
                content += "\n"

        content += """
## Implementation Considerations
- All requirements must be implemented in the specified order
- Security protocols must be strictly followed
- Regular validation of access and configurations is required

## Success Criteria
- All system components are properly configured
- Users can access the system securely
- All functionalities work as specified in the requirements

## Approval
This document requires review and approval from relevant stakeholders before implementation.
"""
        
        logger.info("BRD content generated")
        return content

    def generate_pdf(self, content, pdf_path):
        logger.info(f"Generating PDF at {pdf_path}")
        c = canvas.Canvas(pdf_path, pagesize=letter)
        y = 750
        
        # Improved PDF formatting
        for line in content.split('\n'):
            if line.startswith('# '):
                # Main title
                c.setFont("Helvetica-Bold", 18)
                c.drawString(72, y, line[2:])
                y -= 30
            elif line.startswith('## '):
                # Section headers
                if y < 100:  # Check if we need a new page
                    c.showPage()
                    y = 750
                c.setFont("Helvetica-Bold", 14)
                c.drawString(72, y, line[3:])
                y -= 25
            elif line.startswith('### '):
                # Subsection headers
                if y < 100:
                    c.showPage()
                    y = 750
                c.setFont("Helvetica-Bold", 12)
                c.drawString(72, y, line[4:])
                y -= 20
            elif line.startswith('- '):
                # Bullet points
                if y < 100:
                    c.showPage()
                    y = 750
                c.setFont("Helvetica", 11)
                c.drawString(90, y, '•')
                c.drawString(100, y, line[2:])
                y -= 15
            elif line.startswith(tuple('0123456789')):
                # Numbered points
                if y < 100:
                    c.showPage()
                    y = 750
                c.setFont("Helvetica", 11)
                c.drawString(90, y, line)
                y -= 15
            elif line.strip():
                # Regular text
                if y < 100:
                    c.showPage()
                    y = 750
                c.setFont("Helvetica", 11)
                c.drawString(72, y, line)
                y -= 15
            else:
                # Empty line
                y -= 10
                
            if y < 50:
                c.showPage()
                y = 750
                
        c.save()
        logger.info(f"PDF generated at {pdf_path}")
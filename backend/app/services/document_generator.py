from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT, TA_JUSTIFY
from datetime import datetime
import os
import json
from typing import Dict, Any, Optional
from jinja2 import Template

from app.core.config import settings
from app.models.database import DocumentTemplate, LegalIssue

class DocumentGenerator:
    """Service for generating legal documents in PDF format."""
    
    def __init__(self):
        self.output_dir = settings.pdf_output_dir
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
        
        # Ensure output directory exists
        os.makedirs(self.output_dir, exist_ok=True)
    
    def _setup_custom_styles(self):
        """Set up custom paragraph styles for legal documents."""
        
        # Header style
        self.styles.add(ParagraphStyle(
            name='LegalHeader',
            parent=self.styles['Heading1'],
            fontSize=16,
            spaceAfter=20,
            alignment=TA_CENTER,
            textColor=colors.black
        ))
        
        # Subheader style
        self.styles.add(ParagraphStyle(
            name='LegalSubHeader',
            parent=self.styles['Heading2'],
            fontSize=14,
            spaceAfter=12,
            spaceBefore=12,
            alignment=TA_LEFT,
            textColor=colors.black
        ))
        
        # Body text style
        self.styles.add(ParagraphStyle(
            name='LegalBody',
            parent=self.styles['Normal'],
            fontSize=11,
            spaceAfter=6,
            alignment=TA_JUSTIFY,
            leftIndent=0,
            rightIndent=0
        ))
        
        # Signature style
        self.styles.add(ParagraphStyle(
            name='Signature',
            parent=self.styles['Normal'],
            fontSize=11,
            spaceAfter=6,
            alignment=TA_LEFT,
            leftIndent=0
        ))
        
        # Date style
        self.styles.add(ParagraphStyle(
            name='DateStyle',
            parent=self.styles['Normal'],
            fontSize=11,
            alignment=TA_RIGHT,
            spaceAfter=12
        ))
    
    async def generate_document(
        self,
        template: DocumentTemplate,
        issue: LegalIssue,
        document_type: str,
        custom_data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Generate a legal document based on template and issue data."""
        
        # Prepare template data
        template_data = self._prepare_template_data(issue, custom_data)
        
        # Render template content
        content = self._render_template(template.template_content, template_data)
        
        # Generate filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{document_type}_{issue.id}_{timestamp}.pdf"
        file_path = os.path.join(self.output_dir, filename)
        
        # Generate PDF
        self._create_pdf(content, file_path, template.name)
        
        return {
            "file_path": file_path,
            "file_name": filename,
            "content_data": template_data
        }
    
    def _prepare_template_data(self, issue: LegalIssue, custom_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Prepare data for template rendering."""
        
        data = {
            "current_date": datetime.now().strftime("%B %d, %Y"),
            "issue_description": issue.description,
            "issue_category": issue.category or "General Legal Matter",
            "location": issue.location or "Not specified",
            "urgency": issue.urgency,
            "user_email": issue.user_email or "",
            "issue_id": issue.id,
            "created_date": issue.created_at.strftime("%B %d, %Y") if issue.created_at else ""
        }
        
        # Add custom data if provided
        if custom_data:
            data.update(custom_data)
        
        # Add common legal document fields
        data.update({
            "sender_name": custom_data.get("sender_name", "[YOUR NAME]") if custom_data else "[YOUR NAME]",
            "sender_address": custom_data.get("sender_address", "[YOUR ADDRESS]") if custom_data else "[YOUR ADDRESS]",
            "recipient_name": custom_data.get("recipient_name", "[RECIPIENT NAME]") if custom_data else "[RECIPIENT NAME]",
            "recipient_address": custom_data.get("recipient_address", "[RECIPIENT ADDRESS]") if custom_data else "[RECIPIENT ADDRESS]",
            "case_number": custom_data.get("case_number", "") if custom_data else "",
            "amount": custom_data.get("amount", "") if custom_data else "",
            "deadline": custom_data.get("deadline", "") if custom_data else ""
        })
        
        return data
    
    def _render_template(self, template_content: str, data: Dict[str, Any]) -> str:
        """Render template content with provided data."""
        
        try:
            template = Template(template_content)
            return template.render(**data)
        except Exception as e:
            # Fallback to simple string replacement if Jinja2 fails
            content = template_content
            for key, value in data.items():
                content = content.replace(f"{{{{{key}}}}}", str(value))
            return content
    
    def _create_pdf(self, content: str, file_path: str, document_title: str):
        """Create PDF document from rendered content."""
        
        # Create PDF document
        doc = SimpleDocTemplate(
            file_path,
            pagesize=letter,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=18
        )
        
        # Build document content
        story = []
        
        # Add title
        title = Paragraph(document_title, self.styles['LegalHeader'])
        story.append(title)
        story.append(Spacer(1, 12))
        
        # Add date
        date_text = f"Date: {datetime.now().strftime('%B %d, %Y')}"
        date_para = Paragraph(date_text, self.styles['DateStyle'])
        story.append(date_para)
        story.append(Spacer(1, 12))
        
        # Process content sections
        sections = content.split('\n\n')
        for section in sections:
            if section.strip():
                # Check if section is a header (starts with #)
                if section.strip().startswith('#'):
                    header_text = section.strip().lstrip('#').strip()
                    header_para = Paragraph(header_text, self.styles['LegalSubHeader'])
                    story.append(header_para)
                else:
                    # Regular paragraph
                    para = Paragraph(section.strip(), self.styles['LegalBody'])
                    story.append(para)
                    story.append(Spacer(1, 6))
        
        # Add signature section
        story.append(Spacer(1, 24))
        signature_lines = [
            "Sincerely,",
            "",
            "",
            "_" * 30,
            "[Your Name]",
            "[Your Title/Relationship]"
        ]
        
        for line in signature_lines:
            sig_para = Paragraph(line, self.styles['Signature'])
            story.append(sig_para)
            if line == "":
                story.append(Spacer(1, 12))
        
        # Build PDF
        doc.build(story)
    
    def get_available_templates(self) -> Dict[str, Dict[str, Any]]:
        """Get available document templates with their metadata."""
        
        return {
            "demand_letter": {
                "name": "Demand Letter",
                "description": "General purpose demand letter for various legal issues",
                "required_fields": ["recipient_name", "recipient_address", "amount", "deadline"],
                "template": self._get_demand_letter_template()
            },
            "complaint_letter": {
                "name": "Complaint Letter",
                "description": "Formal complaint letter to businesses or organizations",
                "required_fields": ["recipient_name", "recipient_address", "complaint_details"],
                "template": self._get_complaint_letter_template()
            },
            "notice_letter": {
                "name": "Legal Notice",
                "description": "General legal notice template",
                "required_fields": ["recipient_name", "recipient_address", "notice_details"],
                "template": self._get_notice_letter_template()
            },
            "tenant_demand": {
                "name": "Tenant Demand Letter",
                "description": "Demand letter for tenant rights issues",
                "required_fields": ["landlord_name", "property_address", "issue_details", "deadline"],
                "template": self._get_tenant_demand_template()
            },
            "debt_validation": {
                "name": "Debt Validation Request",
                "description": "Request for debt validation from collectors",
                "required_fields": ["collector_name", "collector_address", "debt_amount", "account_number"],
                "template": self._get_debt_validation_template()
            }
        }
    
    def _get_demand_letter_template(self) -> str:
        """Get demand letter template."""
        return """
{{sender_name}}
{{sender_address}}

{{current_date}}

{{recipient_name}}
{{recipient_address}}

# DEMAND FOR PAYMENT

Dear {{recipient_name}},

This letter serves as formal notice that you owe me the sum of ${{amount}} for {{issue_description}}.

Despite previous attempts to resolve this matter, payment has not been received. This debt is now {{urgency}} and requires immediate attention.

# DEMAND FOR PAYMENT

I hereby demand payment of the full amount of ${{amount}} within {{deadline}} days of receipt of this letter. If payment is not received by this deadline, I will be forced to pursue all available legal remedies, including but not limited to:

- Filing a lawsuit against you for the full amount owed plus interest
- Seeking attorney's fees and court costs
- Reporting this debt to credit reporting agencies
- Pursuing collection through other legal means

# OPPORTUNITY TO RESOLVE

I prefer to resolve this matter without litigation. If you believe this debt is in error or if you would like to discuss payment arrangements, please contact me immediately at {{user_email}} or the address above.

Please be advised that this is an attempt to collect a debt, and any information obtained will be used for that purpose.

Time is of the essence. Please give this matter your immediate attention.
"""
    
    def _get_complaint_letter_template(self) -> str:
        """Get complaint letter template."""
        return """
{{sender_name}}
{{sender_address}}

{{current_date}}

{{recipient_name}}
{{recipient_address}}

# FORMAL COMPLAINT

Dear {{recipient_name}},

I am writing to formally complain about {{issue_description}}.

# DETAILS OF COMPLAINT

{{issue_description}}

This situation occurred on or around {{created_date}} and has caused me significant {{urgency}} concern.

# REQUESTED RESOLUTION

I am requesting that you take the following actions to resolve this matter:

1. Acknowledge receipt of this complaint within 5 business days
2. Investigate the matter thoroughly
3. Provide a written response with your findings and proposed resolution within 15 business days
4. Take appropriate corrective action to prevent similar issues in the future

# NEXT STEPS

If this matter is not resolved satisfactorily within 30 days, I will be forced to pursue other remedies, including filing complaints with relevant regulatory agencies and considering legal action.

I look forward to your prompt response and resolution of this matter.
"""
    
    def _get_notice_letter_template(self) -> str:
        """Get general notice letter template."""
        return """
{{sender_name}}
{{sender_address}}

{{current_date}}

{{recipient_name}}
{{recipient_address}}

# LEGAL NOTICE

Dear {{recipient_name}},

Please be advised that this letter serves as formal legal notice regarding {{issue_description}}.

# NOTICE DETAILS

{{issue_description}}

This matter is classified as {{urgency}} priority and requires your immediate attention.

# REQUIRED ACTION

You are hereby notified that you must take appropriate action to address this matter within a reasonable time period. Failure to respond or take corrective action may result in further legal proceedings.

# LEGAL RIGHTS

Please be aware that you have certain legal rights in this matter. You may wish to consult with an attorney to understand your rights and obligations.

This notice is provided in accordance with applicable laws and regulations. Please treat this matter with the seriousness it deserves.
"""
    
    def _get_tenant_demand_template(self) -> str:
        """Get tenant demand letter template."""
        return """
{{sender_name}}
{{sender_address}}

{{current_date}}

{{recipient_name}} (Landlord)
{{recipient_address}}

# TENANT DEMAND LETTER

Dear {{recipient_name}},

I am your tenant at {{property_address}}. I am writing to formally demand that you address the following issue: {{issue_description}}.

# LANDLORD OBLIGATIONS

As my landlord, you have a legal obligation to maintain the rental property in habitable condition and comply with all applicable housing codes and regulations.

# DEMAND FOR ACTION

I hereby demand that you take the following action within {{deadline}} days of receipt of this letter:

{{issue_description}}

# CONSEQUENCES OF NON-COMPLIANCE

If you fail to address this matter within the specified timeframe, I will be forced to pursue all available legal remedies, including:

- Withholding rent as permitted by law
- Making necessary repairs and deducting costs from rent
- Filing complaints with local housing authorities
- Pursuing legal action for damages
- Terminating the lease due to breach of habitability

# TENANT RIGHTS

Please be advised that I am aware of my rights as a tenant under state and local laws, and I will not hesitate to exercise these rights if necessary.

I prefer to resolve this matter amicably and look forward to your prompt response.
"""
    
    def _get_debt_validation_template(self) -> str:
        """Get debt validation request template."""
        return """
{{sender_name}}
{{sender_address}}

{{current_date}}

{{recipient_name}}
{{recipient_address}}

# DEBT VALIDATION REQUEST

Re: Account Number: {{account_number}}
    Alleged Debt Amount: ${{amount}}

Dear {{recipient_name}},

This letter is sent in response to a notice I received from you on {{created_date}}. Be advised that this is not a refusal to pay, but a notice sent pursuant to the Fair Debt Collection Practices Act, 15 USC 1692g Sec. 809 (b).

# VALIDATION REQUEST

I hereby request that you provide validation of this alleged debt. Please provide the following information:

1. Proof that you are licensed to collect debts in my state
2. Proof of your authority to collect this debt on behalf of the original creditor
3. Complete payment history from the original creditor
4. Copy of the original signed agreement or contract
5. Proof that the statute of limitations has not expired on this account

# LEGAL NOTICE

Until you provide proper validation of this debt, I dispute the validity of this alleged debt in its entirety. You must cease all collection activities until proper validation is provided.

Please be advised that I am recording all communications regarding this matter and will report any violations of the Fair Debt Collection Practices Act to the appropriate authorities.

All future communications regarding this matter must be in writing and sent to the address above.
"""


"""
Database initialization script to populate the database with default templates and resources.
"""

import json
from sqlalchemy.orm import Session
from app.core.database import SessionLocal, engine
from app.models.database import Base, DocumentTemplate, LegalResource

def init_database():
    """Initialize database with default data."""
    
    # Create all tables
    Base.metadata.create_all(bind=engine)
    
    # Create session
    db = SessionLocal()
    
    try:
        # Check if data already exists
        if db.query(DocumentTemplate).first():
            print("Database already initialized with templates.")
            return
        
        # Create document templates
        create_document_templates(db)
        
        # Create legal resources
        create_legal_resources(db)
        
        print("Database initialized successfully!")
        
    except Exception as e:
        print(f"Error initializing database: {e}")
        db.rollback()
    finally:
        db.close()

def create_document_templates(db: Session):
    """Create default document templates."""
    
    templates = [
        {
            "name": "Demand Letter for Payment",
            "category": "debt_collection",
            "description": "General purpose demand letter for payment of debts",
            "template_content": get_demand_letter_template(),
            "required_fields": json.dumps(["recipient_name", "recipient_address", "amount", "deadline"])
        },
        {
            "name": "Consumer Complaint Letter",
            "category": "consumer_protection",
            "description": "Formal complaint letter to businesses about defective products or services",
            "template_content": get_complaint_letter_template(),
            "required_fields": json.dumps(["recipient_name", "recipient_address", "complaint_details"])
        },
        {
            "name": "Tenant Demand for Repairs",
            "category": "tenant_rights",
            "description": "Demand letter for landlord to make necessary repairs",
            "template_content": get_tenant_demand_template(),
            "required_fields": json.dumps(["landlord_name", "property_address", "issue_details", "deadline"])
        },
        {
            "name": "Debt Validation Request",
            "category": "debt_collection",
            "description": "Request for debt validation from collectors under FDCPA",
            "template_content": get_debt_validation_template(),
            "required_fields": json.dumps(["collector_name", "collector_address", "debt_amount", "account_number"])
        },
        {
            "name": "Employment Discrimination Complaint",
            "category": "employment",
            "description": "Formal complaint about workplace discrimination",
            "template_content": get_employment_complaint_template(),
            "required_fields": json.dumps(["employer_name", "employer_address", "incident_details", "witnesses"])
        },
        {
            "name": "Security Deposit Demand",
            "category": "tenant_rights",
            "description": "Letter demanding return of security deposit",
            "template_content": get_security_deposit_template(),
            "required_fields": json.dumps(["landlord_name", "property_address", "deposit_amount", "move_out_date"])
        },
        {
            "name": "Cease and Desist Letter",
            "category": "civil_rights",
            "description": "Letter to stop harassment or unwanted contact",
            "template_content": get_cease_desist_template(),
            "required_fields": json.dumps(["recipient_name", "recipient_address", "harassment_details"])
        },
        {
            "name": "Insurance Claim Appeal",
            "category": "healthcare",
            "description": "Appeal letter for denied insurance claims",
            "template_content": get_insurance_appeal_template(),
            "required_fields": json.dumps(["insurance_company", "policy_number", "claim_number", "denial_reason"])
        }
    ]
    
    for template_data in templates:
        template = DocumentTemplate(**template_data)
        db.add(template)
    
    db.commit()
    print(f"Created {len(templates)} document templates.")

def create_legal_resources(db: Session):
    """Create default legal resources."""
    
    resources = [
        {
            "name": "Legal Aid Society",
            "organization_type": "legal_aid",
            "description": "Provides free legal services to low-income individuals",
            "website": "https://www.legalaid.org",
            "phone": "1-800-LEGAL-AID",
            "jurisdiction": "US",
            "categories": json.dumps(["tenant_rights", "family_law", "immigration", "consumer_protection"])
        },
        {
            "name": "National Consumer Law Center",
            "organization_type": "nonprofit",
            "description": "Consumer advocacy organization providing resources and assistance",
            "website": "https://www.nclc.org",
            "phone": "617-542-8010",
            "jurisdiction": "US",
            "categories": json.dumps(["consumer_protection", "debt_collection", "housing"])
        },
        {
            "name": "Equal Employment Opportunity Commission",
            "organization_type": "government",
            "description": "Federal agency enforcing workplace discrimination laws",
            "website": "https://www.eeoc.gov",
            "phone": "1-800-669-4000",
            "jurisdiction": "US",
            "categories": json.dumps(["employment", "civil_rights"])
        },
        {
            "name": "National Immigration Law Center",
            "organization_type": "nonprofit",
            "description": "Advocacy organization for immigrant rights",
            "website": "https://www.nilc.org",
            "phone": "213-639-3900",
            "jurisdiction": "US",
            "categories": json.dumps(["immigration"])
        },
        {
            "name": "National Domestic Violence Hotline",
            "organization_type": "nonprofit",
            "description": "24/7 support for domestic violence survivors",
            "website": "https://www.thehotline.org",
            "phone": "1-800-799-7233",
            "jurisdiction": "US",
            "categories": json.dumps(["family_law", "civil_rights"])
        },
        {
            "name": "American Civil Liberties Union",
            "organization_type": "nonprofit",
            "description": "Civil liberties advocacy organization",
            "website": "https://www.aclu.org",
            "phone": "212-549-2500",
            "jurisdiction": "US",
            "categories": json.dumps(["civil_rights", "criminal"])
        },
        {
            "name": "National Association of Consumer Advocates",
            "organization_type": "bar_association",
            "description": "Organization of attorneys representing consumers",
            "website": "https://www.consumeradvocates.org",
            "jurisdiction": "US",
            "categories": json.dumps(["consumer_protection", "debt_collection"])
        },
        {
            "name": "HUD Fair Housing Office",
            "organization_type": "government",
            "description": "Federal office enforcing fair housing laws",
            "website": "https://www.hud.gov/fairhousing",
            "phone": "1-800-669-9777",
            "jurisdiction": "US",
            "categories": json.dumps(["housing", "civil_rights"])
        }
    ]
    
    for resource_data in resources:
        resource = LegalResource(**resource_data)
        db.add(resource)
    
    db.commit()
    print(f"Created {len(resources)} legal resources.")

# Template content functions
def get_demand_letter_template():
    return """{{sender_name}}
{{sender_address}}

{{current_date}}

{{recipient_name}}
{{recipient_address}}

# DEMAND FOR PAYMENT

Dear {{recipient_name}},

This letter serves as formal notice that you owe me the sum of ${{amount}} for {{issue_description}}.

Despite previous attempts to resolve this matter, payment has not been received. This debt is now {{urgency}} and requires immediate attention.

I hereby demand payment of the full amount of ${{amount}} within {{deadline}} days of receipt of this letter. If payment is not received by this deadline, I will be forced to pursue all available legal remedies.

Please give this matter your immediate attention."""

def get_complaint_letter_template():
    return """{{sender_name}}
{{sender_address}}

{{current_date}}

{{recipient_name}}
{{recipient_address}}

# FORMAL COMPLAINT

Dear {{recipient_name}},

I am writing to formally complain about {{issue_description}}.

This situation has caused me significant concern and I am requesting that you take appropriate action to resolve this matter.

I look forward to your prompt response and resolution of this issue."""

def get_tenant_demand_template():
    return """{{sender_name}}
{{sender_address}}

{{current_date}}

{{recipient_name}} (Landlord)
{{recipient_address}}

# TENANT DEMAND LETTER

Dear {{recipient_name}},

I am your tenant at {{property_address}}. I am writing to formally demand that you address the following issue: {{issue_description}}.

As my landlord, you have a legal obligation to maintain the rental property in habitable condition.

I hereby demand that you take appropriate action within {{deadline}} days of receipt of this letter."""

def get_debt_validation_template():
    return """{{sender_name}}
{{sender_address}}

{{current_date}}

{{recipient_name}}
{{recipient_address}}

# DEBT VALIDATION REQUEST

Re: Account Number: {{account_number}}
    Alleged Debt Amount: ${{amount}}

This letter is sent pursuant to the Fair Debt Collection Practices Act, 15 USC 1692g Sec. 809 (b).

I hereby request that you provide validation of this alleged debt. Until you provide proper validation, I dispute the validity of this alleged debt in its entirety."""

def get_employment_complaint_template():
    return """{{sender_name}}
{{sender_address}}

{{current_date}}

{{recipient_name}}
{{recipient_address}}

# EMPLOYMENT DISCRIMINATION COMPLAINT

Dear {{recipient_name}},

I am writing to formally complain about discrimination I have experienced in the workplace.

{{issue_description}}

I request that you investigate this matter thoroughly and take appropriate corrective action."""

def get_security_deposit_template():
    return """{{sender_name}}
{{sender_address}}

{{current_date}}

{{recipient_name}} (Landlord)
{{recipient_address}}

# DEMAND FOR RETURN OF SECURITY DEPOSIT

Dear {{recipient_name}},

I was your tenant at {{property_address}} until {{move_out_date}}.

I hereby demand the return of my security deposit in the amount of ${{deposit_amount}} within the time period required by law."""

def get_cease_desist_template():
    return """{{sender_name}}
{{sender_address}}

{{current_date}}

{{recipient_name}}
{{recipient_address}}

# CEASE AND DESIST NOTICE

Dear {{recipient_name}},

This letter serves as formal notice to CEASE AND DESIST from {{harassment_details}}.

Your actions constitute harassment and must stop immediately. Continued contact will result in legal action."""

def get_insurance_appeal_template():
    return """{{sender_name}}
{{sender_address}}

{{current_date}}

{{recipient_name}}
{{recipient_address}}

# INSURANCE CLAIM APPEAL

Re: Policy Number: {{policy_number}}
    Claim Number: {{claim_number}}

I am formally appealing your denial of my insurance claim.

The denial reason given was: {{denial_reason}}

I believe this denial is incorrect and request that you reconsider this decision."""

if __name__ == "__main__":
    init_database()


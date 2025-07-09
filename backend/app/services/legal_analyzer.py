from typing import Dict, List, Any, Optional
from app.services.llm_service import LLMService
from app.models.schemas import LegalCategory, DocumentType

class LegalAnalyzer:
    """High-level legal analysis service that coordinates LLM calls and business logic."""
    
    def __init__(self):
        self.llm_service = LLMService()
        self.category_templates = self._load_category_templates()
    
    async def analyze_issue(self, description: str, location: Optional[str] = None) -> Dict[str, Any]:
        """Perform comprehensive analysis of a legal issue."""
        
        try:
            # First, classify the legal domain
            print(f"Analyzing issue: {description[:100]}...")
            
            classification = await self.llm_service.classify_legal_domain(description, location)
            
            print(f"Classification result: {classification}")
            
            # Validate classification result
            if not classification or not isinstance(classification, dict):
                print("Invalid classification result, using default")
                classification = {
                    "category": "other",
                    "confidence": 0.1,
                    "urgency": "medium",
                    "complexity": "moderate"
                }
            
            category = classification.get("category", "other")
            
            # Get suggested actions based on category
            suggested_actions = self._get_suggested_actions(category)
            
            # Get relevant document templates
            relevant_templates = self._get_relevant_templates(category)
            
            result = {
                "category": category,
                "confidence": classification.get("confidence", 0.1),
                "urgency": classification.get("urgency", "medium"),
                "complexity": classification.get("complexity", "moderate"),
                "suggested_actions": suggested_actions,
                "relevant_templates": relevant_templates,
                "reasoning": classification.get("reasoning", "")
            }
            
            print(f"Final analysis result: {result}")
            return result
            
        except Exception as e:
            print(f"Error in analyze_issue: {str(e)}")
            # Return a safe default
            return {
                "category": "other",
                "confidence": 0.1,
                "urgency": "medium",
                "complexity": "moderate",
                "suggested_actions": self._get_suggested_actions("other"),
                "relevant_templates": self._get_relevant_templates("other"),
                "reasoning": f"Analysis error: {str(e)}"
            }
    
    def _get_suggested_actions(self, category: str) -> List[str]:
        """Get category-specific suggested actions."""
        
        action_map = {
            "tenant_rights": [
                "Document all communications with your landlord",
                "Take photos of any housing condition issues",
                "Review your lease agreement carefully",
                "Contact your local tenant rights organization",
                "Check if your area has rent control or tenant protection laws"
            ],
            "consumer_protection": [
                "Gather all documentation related to the transaction",
                "Contact the business to attempt resolution",
                "File a complaint with your state's consumer protection agency",
                "Consider disputing charges with your credit card company",
                "Report scams to the Federal Trade Commission (FTC)"
            ],
            "employment": [
                "Document all incidents with dates and witnesses",
                "Review your employee handbook and contract",
                "File a complaint with HR if appropriate",
                "Contact the Equal Employment Opportunity Commission (EEOC)",
                "Consult with an employment attorney"
            ],
            "family_law": [
                "Gather important documents (marriage certificate, financial records)",
                "Consider mediation before litigation",
                "Prioritize the best interests of any children involved",
                "Consult with a family law attorney",
                "Look into local family court self-help resources"
            ],
            "immigration": [
                "Gather all immigration documents and records",
                "Do not sign anything without understanding it fully",
                "Contact a qualified immigration attorney immediately",
                "Reach out to local immigrant rights organizations",
                "Know your rights if contacted by immigration enforcement"
            ],
            "criminal": [
                "Exercise your right to remain silent",
                "Request an attorney immediately",
                "Do not discuss your case with anyone except your lawyer",
                "Gather character references and documentation",
                "Contact a public defender if you cannot afford an attorney"
            ],
            "civil_rights": [
                "Document the discriminatory incident thoroughly",
                "File a complaint with the appropriate civil rights agency",
                "Gather witness statements and evidence",
                "Contact civil rights organizations for support",
                "Consider consulting with a civil rights attorney"
            ],
            "debt_collection": [
                "Request debt validation in writing",
                "Know your rights under the Fair Debt Collection Practices Act",
                "Keep detailed records of all communications",
                "Consider debt consolidation or payment plans",
                "Consult with a bankruptcy attorney if overwhelmed"
            ],
            "housing": [
                "Document any discriminatory treatment",
                "File a complaint with HUD or local fair housing agency",
                "Know your rights under the Fair Housing Act",
                "Seek assistance from local housing advocacy groups",
                "Consider consulting with a housing attorney"
            ],
            "healthcare": [
                "Request itemized bills and medical records",
                "Appeal insurance denials in writing",
                "Contact your state's insurance commissioner",
                "Seek assistance from patient advocacy organizations",
                "Consider consulting with a healthcare attorney"
            ]
        }
        
        return action_map.get(category, [
            "Gather all relevant documentation",
            "Contact local legal aid organizations",
            "Consult with a qualified attorney",
            "Research your rights and options",
            "Consider alternative dispute resolution"
        ])
    
    def _get_relevant_templates(self, category: str) -> List[Dict[str, Any]]:
        """Get relevant document templates for a category."""
        
        template_map = {
            "tenant_rights": [
                {
                    "id": 1, 
                    "name": "Demand Letter for Repairs", 
                    "category": "tenant_rights", 
                    "description": "Letter demanding landlord make necessary repairs",
                    "required_fields": ["tenant_name", "landlord_name", "property_address", "issue_description", "repair_deadline"]
                },
                {
                    "id": 2, 
                    "name": "Notice to Quit Response", 
                    "category": "tenant_rights", 
                    "description": "Response to eviction notice",
                    "required_fields": ["tenant_name", "landlord_name", "property_address", "notice_date", "response_reason"]
                },
                {
                    "id": 3, 
                    "name": "Security Deposit Demand", 
                    "category": "tenant_rights", 
                    "description": "Letter demanding return of security deposit",
                    "required_fields": ["tenant_name", "landlord_name", "property_address", "move_out_date", "deposit_amount"]
                }
            ],
            "consumer_protection": [
                {
                    "id": 4, 
                    "name": "Consumer Complaint Letter", 
                    "category": "consumer_protection", 
                    "description": "Formal complaint to business about defective product or service",
                    "required_fields": ["consumer_name", "business_name", "product_service", "issue_description", "resolution_requested"]
                },
                {
                    "id": 5, 
                    "name": "Debt Dispute Letter", 
                    "category": "consumer_protection", 
                    "description": "Letter disputing incorrect charges or billing",
                    "required_fields": ["consumer_name", "creditor_name", "account_number", "disputed_amount", "dispute_reason"]
                },
                {
                    "id": 6, 
                    "name": "Warranty Claim Letter", 
                    "category": "consumer_protection", 
                    "description": "Letter claiming warranty coverage",
                    "required_fields": ["consumer_name", "manufacturer", "product_model", "purchase_date", "warranty_issue"]
                }
            ],
            "employment": [
                {
                    "id": 7, 
                    "name": "Workplace Discrimination Complaint", 
                    "category": "employment", 
                    "description": "Formal complaint about workplace discrimination",
                    "required_fields": ["employee_name", "employer_name", "discrimination_type", "incident_date", "witnesses"]
                },
                {
                    "id": 8, 
                    "name": "Wage Claim Letter", 
                    "category": "employment", 
                    "description": "Letter demanding unpaid wages",
                    "required_fields": ["employee_name", "employer_name", "work_period", "unpaid_amount", "hours_worked"]
                },
                {
                    "id": 9, 
                    "name": "FMLA Request", 
                    "category": "employment", 
                    "description": "Request for Family and Medical Leave",
                    "required_fields": ["employee_name", "employer_name", "leave_start_date", "leave_duration", "medical_reason"]
                }
            ],
            "debt_collection": [
                {
                    "id": 10, 
                    "name": "Debt Validation Request", 
                    "category": "debt_collection", 
                    "description": "Letter requesting validation of debt",
                    "required_fields": ["debtor_name", "collector_name", "account_number", "alleged_debt_amount", "original_creditor"]
                },
                {
                    "id": 11, 
                    "name": "Cease and Desist Letter", 
                    "category": "debt_collection", 
                    "description": "Letter to stop harassment by debt collectors",
                    "required_fields": ["debtor_name", "collector_name", "account_number", "harassment_description", "cease_request"]
                },
                {
                    "id": 12, 
                    "name": "Payment Plan Proposal", 
                    "category": "debt_collection", 
                    "description": "Proposal for payment arrangement",
                    "required_fields": ["debtor_name", "creditor_name", "total_debt", "proposed_payment", "payment_schedule"]
                }
            ],
            "family_law": [
                {
                    "id": 14, 
                    "name": "Child Custody Petition", 
                    "category": "family_law", 
                    "description": "Petition for child custody arrangement",
                    "required_fields": ["parent_name", "other_parent_name", "child_names", "custody_type", "reasons"]
                },
                {
                    "id": 15, 
                    "name": "Divorce Settlement Agreement", 
                    "category": "family_law", 
                    "description": "Agreement for divorce settlement terms",
                    "required_fields": ["spouse1_name", "spouse2_name", "marriage_date", "assets", "custody_arrangement"]
                }
            ],
            "immigration": [
                {
                    "id": 16, 
                    "name": "Immigration Appeal Letter", 
                    "category": "immigration", 
                    "description": "Appeal letter for immigration decision",
                    "required_fields": ["applicant_name", "case_number", "decision_date", "appeal_grounds", "supporting_evidence"]
                }
            ],
            "criminal": [
                {
                    "id": 17, 
                    "name": "Expungement Petition", 
                    "category": "criminal", 
                    "description": "Petition to expunge criminal record",
                    "required_fields": ["petitioner_name", "case_number", "conviction_date", "offense_type", "rehabilitation_evidence"]
                }
            ],
            "civil_rights": [
                {
                    "id": 18, 
                    "name": "Discrimination Complaint", 
                    "category": "civil_rights", 
                    "description": "Formal complaint about discrimination",
                    "required_fields": ["complainant_name", "respondent_name", "discrimination_basis", "incident_description", "witnesses"]
                }
            ],
            "housing": [
                {
                    "id": 19, 
                    "name": "Fair Housing Complaint", 
                    "category": "housing", 
                    "description": "Complaint about housing discrimination",
                    "required_fields": ["complainant_name", "property_owner", "property_address", "discrimination_type", "incident_date"]
                }
            ],
            "healthcare": [
                {
                    "id": 20, 
                    "name": "Insurance Appeal Letter", 
                    "category": "healthcare", 
                    "description": "Appeal letter for insurance claim denial",
                    "required_fields": ["patient_name", "insurance_company", "claim_number", "denial_reason", "medical_justification"]
                }
            ]
        }
        
        return template_map.get(category, [
            {
                "id": 13, 
                "name": "General Legal Notice", 
                "category": "other", 
                "description": "General purpose legal notice template",
                "required_fields": ["sender_name", "recipient_name", "notice_subject", "notice_body", "signature_date"]
            }
        ])
    
    def _load_category_templates(self) -> Dict[str, Dict[str, Any]]:
        """Load category-specific prompt templates and guidance."""
        
        return {
            "tenant_rights": {
                "description": "Landlord-tenant disputes, evictions, housing conditions",
                "key_laws": ["Fair Housing Act", "State Landlord-Tenant Laws", "Local Housing Codes"],
                "common_issues": ["Eviction notices", "Security deposit disputes", "Habitability issues", "Rent increases"],
                "urgency_factors": ["Eviction timeline", "Health and safety issues", "Illegal lockouts"]
            },
            "consumer_protection": {
                "description": "Fraud, scams, unfair business practices",
                "key_laws": ["Fair Credit Reporting Act", "Truth in Lending Act", "State Consumer Protection Laws"],
                "common_issues": ["Defective products", "Billing disputes", "Warranty issues", "Fraudulent charges"],
                "urgency_factors": ["Time limits for disputes", "Ongoing financial harm", "Identity theft"]
            },
            "employment": {
                "description": "Workplace issues, discrimination, wage disputes",
                "key_laws": ["Title VII", "Americans with Disabilities Act", "Fair Labor Standards Act", "Family and Medical Leave Act"],
                "common_issues": ["Discrimination", "Harassment", "Wrongful termination", "Wage theft"],
                "urgency_factors": ["Filing deadlines", "Ongoing harassment", "Financial hardship"]
            },
            "family_law": {
                "description": "Divorce, custody, domestic relations",
                "key_laws": ["State Family Codes", "Uniform Child Custody Jurisdiction Act", "Violence Against Women Act"],
                "common_issues": ["Divorce proceedings", "Child custody", "Domestic violence", "Child support"],
                "urgency_factors": ["Safety concerns", "Child welfare", "Court deadlines"]
            },
            "immigration": {
                "description": "Immigration status, deportation, asylum",
                "key_laws": ["Immigration and Nationality Act", "Asylum laws", "DACA regulations"],
                "common_issues": ["Deportation proceedings", "Asylum claims", "Family reunification", "Work authorization"],
                "urgency_factors": ["Deportation timeline", "Asylum deadlines", "Detention issues"]
            },
            "criminal": {
                "description": "Criminal defense, expungement, rights",
                "key_laws": ["Constitutional rights", "State criminal codes", "Sentencing guidelines"],
                "common_issues": ["Criminal charges", "Bail hearings", "Plea negotiations", "Expungement"],
                "urgency_factors": ["Court dates", "Custody issues", "Statute of limitations"]
            },
            "civil_rights": {
                "description": "Discrimination, civil liberties violations",
                "key_laws": ["Civil Rights Act", "Americans with Disabilities Act", "Constitutional amendments"],
                "common_issues": ["Discrimination", "Police misconduct", "Voting rights", "Accessibility"],
                "urgency_factors": ["Filing deadlines", "Ongoing violations", "Evidence preservation"]
            },
            "debt_collection": {
                "description": "Debt disputes, bankruptcy, creditor harassment",
                "key_laws": ["Fair Debt Collection Practices Act", "Fair Credit Reporting Act", "Bankruptcy Code"],
                "common_issues": ["Debt validation", "Harassment", "Wage garnishment", "Bankruptcy"],
                "urgency_factors": ["Garnishment proceedings", "Foreclosure timeline", "Bankruptcy deadlines"]
            },
            "housing": {
                "description": "Housing discrimination, accessibility, public housing",
                "key_laws": ["Fair Housing Act", "Americans with Disabilities Act", "Section 8 regulations"],
                "common_issues": ["Housing discrimination", "Accessibility modifications", "Public housing issues"],
                "urgency_factors": ["Eviction proceedings", "Safety issues", "Discrimination timeline"]
            },
            "healthcare": {
                "description": "Medical bills, insurance disputes, patient rights",
                "key_laws": ["HIPAA", "Affordable Care Act", "Emergency Medical Treatment and Labor Act"],
                "common_issues": ["Insurance denials", "Medical billing", "Patient rights", "Privacy violations"],
                "urgency_factors": ["Treatment needs", "Appeal deadlines", "Financial hardship"]
            }
        }
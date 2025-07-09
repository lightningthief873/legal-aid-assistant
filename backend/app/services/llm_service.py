from openai import AsyncOpenAI
from app.core.config import settings
aclient = AsyncOpenAI(api_key=settings.openai_api_key)
import httpx
import json
import re
from typing import Dict, List, Optional, Any


class LLMService:
    """Service for interacting with Language Learning Models (OpenAI or local)."""

    def __init__(self):
        if settings.openai_api_key:
            self.use_local = settings.use_local_llm
            self.local_url = settings.local_llm_url

    async def generate_advice(
        self, 
        description: str, 
        category: str, 
        location: Optional[str] = None,
        additional_context: Optional[str] = None
    ) -> Dict[str, Any]:
        """Generate legal advice for a given issue."""

        prompt = self._build_advice_prompt(description, category, location, additional_context)

        try:
            if self.use_local and self.local_url:
                response = await self._call_local_llm(prompt)
            else:
                response = await self._call_openai(prompt)

            return self._parse_advice_response(response)

        except Exception as e:
            return {
                "advice": f"I apologize, but I'm unable to generate advice at this time due to a technical issue: {str(e)}",
                "next_steps": ["Contact a local legal aid organization for assistance"],
                "relevant_laws": [],
                "confidence": 0.0,
                "model_used": "error_fallback"
            }

    async def classify_legal_domain(self, description: str, location: Optional[str] = None) -> Dict[str, Any]:
        """Classify the legal domain of an issue."""

        prompt = self._build_classification_prompt(description, location)

        try:
            if self.use_local and self.local_url:
                response = await self._call_local_llm(prompt)
            else:
                response = await self._call_openai(prompt)

            # Debug logging
            print(f"LLM Response for classification: {response}")
            
            result = self._parse_classification_response(response)
            
            # Debug logging
            print(f"Parsed classification result: {result}")
            
            return result

        except Exception as e:
            print(f"Error in classify_legal_domain: {str(e)}")
            return {
                "category": "other",
                "confidence": 0.0,
                "urgency": "medium",
                "complexity": "moderate",
                "reasoning": f"Classification error: {str(e)}"
            }

    async def _call_openai(self, prompt: str) -> str:
        """Call OpenAI API."""
        try:
            response = await aclient.chat.completions.create(
                model=settings.openai_model,
                messages=[
                    {
                        "role": "system", 
                        "content": "You are a legal classification expert. You must respond with valid JSON only. Do not include any text outside the JSON response."
                    },
                    {"role": "user", "content": prompt}
                ],
                max_tokens=settings.openai_max_tokens,
                temperature=0.1  # Lower temperature for more consistent classification
            )
            return response.choices[0].message.content
        except Exception as e:
            raise Exception(f"OpenAI API error: {str(e)}")

    async def _call_local_llm(self, prompt: str) -> str:
        """Call local LLM endpoint."""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    self.local_url,
                    json={
                        "prompt": prompt,
                        "max_tokens": settings.openai_max_tokens,
                        "temperature": 0.1
                    },
                    timeout=30.0
                )
                response.raise_for_status()
                return response.json().get("response", "")
        except Exception as e:
            raise Exception(f"Local LLM error: {str(e)}")

    def _build_advice_prompt(
        self, 
        description: str, 
        category: str, 
        location: Optional[str] = None,
        additional_context: Optional[str] = None
    ) -> str:
        """Build prompt for legal advice generation."""

        location_text = f" in {location}" if location else ""
        context_text = f"\n\nAdditional context: {additional_context}" if additional_context else ""

        prompt = f"""
You are a legal aid assistant helping someone with a {category} issue{location_text}. 

Issue description: {description}{context_text}

Please provide helpful guidance in the following JSON format:
{{
    "advice": "Detailed advice and explanation of the situation",
    "next_steps": ["Step 1", "Step 2", "Step 3"],
    "relevant_laws": ["Law or regulation 1", "Law or regulation 2"],
    "confidence": 0.85,
    "disclaimers": ["This is not legal advice", "Consult with a qualified attorney"]
}}

Focus on:
1. Explaining the person's rights and options
2. Providing practical next steps they can take
3. Mentioning relevant laws or regulations
4. Being empathetic and supportive
5. Always including appropriate disclaimers

Remember: This is general information only, not legal advice. The person should consult with a qualified attorney for their specific situation.
"""
        return prompt

    def _build_classification_prompt(self, description: str, location: Optional[str] = None) -> str:
        """Build prompt for legal domain classification."""

        location_text = f" in {location}" if location else ""

        prompt = f"""You are a legal classification expert. Analyze this legal issue{location_text} and classify it into the most appropriate category.

Issue description: {description}

IMPORTANT: You must choose from one of these exact categories:
- tenant_rights: Landlord-tenant disputes, evictions, housing conditions, rent issues, lease problems, security deposits, repairs, habitability
- consumer_protection: Fraud, scams, unfair business practices, defective products, billing disputes, warranty issues, identity theft
- employment: Workplace discrimination, harassment, wrongful termination, wage theft, workplace safety, labor violations, FMLA
- family_law: Divorce, child custody, child support, domestic violence, adoption, paternity, marriage, separation
- immigration: Immigration status, deportation, asylum, visas, green cards, citizenship, work permits, family reunification
- criminal: Criminal charges, arrest, bail, plea bargains, expungement, criminal defense, probation, parole
- civil_rights: Discrimination based on race/gender/religion/disability, police misconduct, voting rights, accessibility
- debt_collection: Debt disputes, bankruptcy, creditor harassment, wage garnishment, foreclosure, debt validation
- housing: Housing discrimination, fair housing violations, accessibility issues, public housing, Section 8
- healthcare: Medical bills, insurance disputes, patient rights, HIPAA violations, medical malpractice, insurance denials
- other: Only use this if the issue truly doesn't fit any of the above categories

Classification Guidelines:
- If it involves a landlord and tenant relationship, use "tenant_rights"
- If it involves workplace issues, use "employment"
- If it involves buying/selling goods or services, use "consumer_protection"
- If it involves family relationships, use "family_law"
- If it involves immigration status, use "immigration"
- If it involves criminal charges, use "criminal"
- If it involves discrimination, use "civil_rights"
- If it involves debt or money owed, use "debt_collection"
- If it involves housing discrimination, use "housing"
- If it involves medical/health insurance, use "healthcare"

Respond with ONLY this JSON format (no additional text):
{{
    "category": "exact_category_name",
    "confidence": 0.85,
    "urgency": "low",
    "complexity": "moderate",
    "reasoning": "Brief explanation of why this category was chosen"
}}

Urgency levels: low, medium, high
Complexity levels: simple, moderate, complex
"""
        return prompt

    def _parse_advice_response(self, response: str) -> Dict[str, Any]:
        """Parse and validate advice response."""
        try:
            # Try to extract JSON from response
            start_idx = response.find('{')
            end_idx = response.rfind('}') + 1
            if start_idx != -1 and end_idx != 0:
                json_str = response[start_idx:end_idx]
                data = json.loads(json_str)

                return {
                    "advice": data.get("advice", "Unable to generate advice"),
                    "next_steps": data.get("next_steps", []),
                    "relevant_laws": data.get("relevant_laws", []),
                    "confidence": float(data.get("confidence", 0.5)),
                    "model_used": settings.openai_model if not self.use_local else "local_llm"
                }
            else:
                # Fallback if JSON parsing fails
                return {
                    "advice": response,
                    "next_steps": ["Contact a local legal aid organization"],
                    "relevant_laws": [],
                    "confidence": 0.5,
                    "model_used": settings.openai_model if not self.use_local else "local_llm"
                }
        except Exception:
            return {
                "advice": response if response else "Unable to generate advice",
                "next_steps": ["Contact a local legal aid organization"],
                "relevant_laws": [],
                "confidence": 0.3,
                "model_used": settings.openai_model if not self.use_local else "local_llm"
            }

    def _parse_classification_response(self, response: str) -> Dict[str, Any]:
        """Parse and validate classification response."""
        
        # Valid categories
        valid_categories = [
            "tenant_rights", "consumer_protection", "employment", "family_law",
            "immigration", "criminal", "civil_rights", "debt_collection",
            "housing", "healthcare", "other"
        ]
        
        try:
            # Clean the response
            response = response.strip()
            
            # Try to find JSON in the response
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                json_str = json_match.group(0)
                data = json.loads(json_str)
                
                # Validate the category
                category = data.get("category", "other")
                if category not in valid_categories:
                    print(f"Invalid category '{category}' returned, defaulting to 'other'")
                    category = "other"
                
                # Validate other fields
                confidence = data.get("confidence", 0.5)
                if not isinstance(confidence, (int, float)) or confidence < 0 or confidence > 1:
                    confidence = 0.5
                
                urgency = data.get("urgency", "medium")
                if urgency not in ["low", "medium", "high"]:
                    urgency = "medium"
                
                complexity = data.get("complexity", "moderate")
                if complexity not in ["simple", "moderate", "complex"]:
                    complexity = "moderate"

                return {
                    "category": category,
                    "confidence": float(confidence),
                    "urgency": urgency,
                    "complexity": complexity,
                    "reasoning": data.get("reasoning", "")
                }
            else:
                print(f"No JSON found in response: {response}")
                return {
                    "category": "other",
                    "confidence": 0.3,
                    "urgency": "medium",
                    "complexity": "moderate",
                    "reasoning": "Unable to parse classification response"
                }
        except json.JSONDecodeError as e:
            print(f"JSON decode error: {e}")
            return {
                "category": "other",
                "confidence": 0.1,
                "urgency": "medium",
                "complexity": "moderate",
                "reasoning": f"JSON parsing error: {str(e)}"
            }
        except Exception as e:
            print(f"General parsing error: {e}")
            return {
                "category": "other",
                "confidence": 0.1,
                "urgency": "medium",
                "complexity": "moderate",
                "reasoning": f"Classification error: {str(e)}"
            }
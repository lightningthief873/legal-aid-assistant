import openai
import httpx
import json
from typing import Dict, List, Optional, Any
from app.core.config import settings

class LLMService:
    """Service for interacting with Language Learning Models (OpenAI or local)."""
    
    def __init__(self):
        if settings.openai_api_key:
            openai.api_key = settings.openai_api_key
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
            
            return self._parse_classification_response(response)
            
        except Exception as e:
            return {
                "category": "other",
                "confidence": 0.0,
                "urgency": "medium",
                "complexity": "moderate"
            }
    
    async def _call_openai(self, prompt: str) -> str:
        """Call OpenAI API."""
        try:
            response = await openai.ChatCompletion.acreate(
                model=settings.openai_model,
                messages=[
                    {"role": "system", "content": "You are a helpful legal assistant providing guidance on common legal issues. Always remind users that this is not legal advice and they should consult with a qualified attorney for their specific situation."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=settings.openai_max_tokens,
                temperature=settings.openai_temperature
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
                        "temperature": settings.openai_temperature
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
        
        prompt = f"""
Analyze this legal issue{location_text} and classify it into the appropriate category.

Issue description: {description}

Available categories:
- tenant_rights: Landlord-tenant disputes, evictions, housing conditions
- consumer_protection: Fraud, scams, unfair business practices
- employment: Workplace issues, discrimination, wage disputes
- family_law: Divorce, custody, domestic relations
- immigration: Immigration status, deportation, asylum
- criminal: Criminal defense, expungement, rights
- civil_rights: Discrimination, civil liberties violations
- debt_collection: Debt disputes, bankruptcy, creditor harassment
- housing: Housing discrimination, accessibility, public housing
- healthcare: Medical bills, insurance disputes, patient rights
- other: Issues that don't fit the above categories

Respond in JSON format:
{{
    "category": "category_name",
    "confidence": 0.85,
    "urgency": "low|medium|high",
    "complexity": "simple|moderate|complex",
    "reasoning": "Brief explanation of classification"
}}

Consider:
- Urgency: How time-sensitive is this issue?
- Complexity: How complex is this legal matter?
- Confidence: How certain are you about the classification?
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
        try:
            # Try to extract JSON from response
            start_idx = response.find('{')
            end_idx = response.rfind('}') + 1
            if start_idx != -1 and end_idx != 0:
                json_str = response[start_idx:end_idx]
                data = json.loads(json_str)
                
                return {
                    "category": data.get("category", "other"),
                    "confidence": float(data.get("confidence", 0.5)),
                    "urgency": data.get("urgency", "medium"),
                    "complexity": data.get("complexity", "moderate"),
                    "reasoning": data.get("reasoning", "")
                }
            else:
                return {
                    "category": "other",
                    "confidence": 0.3,
                    "urgency": "medium",
                    "complexity": "moderate",
                    "reasoning": "Unable to classify"
                }
        except Exception:
            return {
                "category": "other",
                "confidence": 0.1,
                "urgency": "medium",
                "complexity": "moderate",
                "reasoning": "Classification error"
            }


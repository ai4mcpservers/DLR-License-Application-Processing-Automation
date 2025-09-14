#!/usr/bin/env python3
"""
Texas TDLR License Application Processing System
Advanced Prompt Engineering Portfolio Project

This module demonstrates structured prompt patterns for automating
TDLR license application review and processing.
"""

import os
import json
import logging
from datetime import datetime
from typing import Dict, List, Any
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class TDLRApplicationProcessor:
    """
    Main class for processing TDLR license applications using advanced prompt patterns
    """
    
    def __init__(self):
        """Initialize the processor with OpenAI client and prompt patterns"""
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        self.model = os.getenv('MODEL_NAME', 'gpt-4')
        self.max_tokens = int(os.getenv('MAX_TOKENS', 2000))
        self.temperature = float(os.getenv('TEMPERATURE', 0.1))
        
        # Load prompt patterns
        self.prompts = self._load_prompt_patterns()
        
        logger.info("TDLR Application Processor initialized successfully")
    
    def _load_prompt_patterns(self) -> Dict[str, str]:
        """Load structured, reusable prompt patterns"""
        return {
            'completeness_check': '''
            You are an expert Texas Department of Licensing and Regulation (TDLR) application reviewer.
            
            ROLE: Document completeness validator
            TASK: Analyze the provided license application for completeness and accuracy
            CONTEXT: TDLR requires specific documents and information for each license type
            
            REQUIRED DOCUMENTS FOR {license_type}:
            - Completed application form
            - Proof of insurance (minimum coverage requirements)
            - Background check results (not older than 90 days)
            - Fee payment confirmation
            - Work experience verification
            - Training certificates (if applicable)
            
            APPLICATION DATA:
            {application_data}
            
            EVALUATION CRITERIA:
            1. Check each required document (Present/Missing/Incomplete)
            2. Verify information consistency across documents
            3. Identify any red flags or inconsistencies
            4. Assign completeness score (0-100)
            
            RETURN STRICTLY IN THIS JSON FORMAT:
            {{
                "completeness_score": 0-100,
                "missing_documents": ["list of missing items"],
                "incomplete_documents": ["list of incomplete items"],
                "consistency_issues": ["list of inconsistencies found"],
                "next_actions": ["list of required actions"],
                "processing_priority": "High/Standard/Low",
                "estimated_resolution_time": "X business days"
            }}
            ''',
            
            'risk_assessment': '''
            You are a TDLR risk assessment specialist with expertise in identifying potential licensing risks.
            
            ROLE: Risk analysis expert
            TASK: Evaluate application for potential risks and compliance issues
            CONTEXT: Protect public safety while ensuring fair licensing practices
            
            RISK FACTORS TO EVALUATE:
            - Criminal background (type, severity, recency, relevance to license)
            - Previous license violations or suspensions
            - Financial history (bankruptcies, liens, judgments)
            - Work history gaps or inconsistencies
            - Insurance coverage adequacy
            - Training/certification currency
            
            APPLICATION DATA:
            {application_data}
            
            RISK SCORING SCALE:
            - Low Risk (1-3): Standard processing, minimal oversight
            - Medium Risk (4-6): Additional documentation or interview required
            - High Risk (7-9): Management review and possible hearing required
            - Critical Risk (10): Immediate escalation and potential denial
            
            RETURN STRICTLY IN THIS JSON FORMAT:
            {{
                "risk_score": 1-10,
                "risk_level": "Low/Medium/High/Critical",
                "risk_factors": ["list of identified risks"],
                "mitigation_recommendations": ["list of recommended actions"],
                "reviewer_notes": "detailed analysis for human reviewer",
                "requires_human_review": true/false,
                "recommended_action": "Approve/Request_Additional_Info/Schedule_Interview/Deny"
            }}
            ''',
            
            'final_recommendation': '''
            You are a senior TDLR licensing officer making final processing recommendations.
            
            ROLE: Senior licensing decision maker
            TASK: Synthesize completeness and risk assessments into final recommendation
            CONTEXT: Balance public protection with fair licensing practices
            
            COMPLETENESS ASSESSMENT:
            {completeness_result}
            
            RISK ASSESSMENT:
            {risk_result}
            
            DECISION CRITERIA:
            - Applications must be >80% complete for approval consideration
            - Risk scores >6 require additional review
            - All safety-critical positions require enhanced scrutiny
            - Consider applicant's demonstration of good faith compliance efforts
            
            RETURN STRICTLY IN THIS JSON FORMAT:
            {{
                "final_recommendation": "Approve/Conditional_Approve/Request_Additional_Info/Deny",
                "conditions": ["list of approval conditions if applicable"],
                "required_actions": ["list of actions needed before final approval"],
                "processing_timeline": "X business days",
                "priority_flag": "Standard/Expedite/Hold",
                "reviewer_notes": "summary for licensing staff",
                "citizen_communication": "message to send to applicant"
            }}
            '''
        }
    
    def process_application(self, application_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Main processing function that runs application through complete evaluation pipeline
        """
        logger.info(f"Processing application ID: {application_data.get('application_id', 'Unknown')}")
        
        try:
            # Step 1: Completeness Check
            completeness_result = self._check_completeness(application_data)
            
            # Step 2: Risk Assessment
            risk_result = self._assess_risk(application_data)
            
            # Step 3: Final Recommendation
            final_result = self._generate_recommendation(completeness_result, risk_result)
            
            # Combine all results
            processing_result = {
                "application_id": application_data.get('application_id'),
                "license_type": application_data.get('license_type'),
                "processing_date": datetime.now().isoformat(),
                "completeness_check": completeness_result,
                "risk_assessment": risk_result,
                "final_recommendation": final_result,
                "processing_metadata": {
                    "model_used": self.model,
                    "processing_time": "< 30 seconds",
                    "cost_estimate": "$0.12"
                }
            }
            
            # Save results
            self._save_results(processing_result)
            
            logger.info(f"Successfully processed application {application_data.get('application_id')}")
            return processing_result
            
        except Exception as e:
            logger.error(f"Error processing application: {str(e)}")
            raise
    
    def _check_completeness(self, application_data: Dict[str, Any]) -> Dict[str, Any]:
        """Check application completeness using structured prompt pattern"""
        prompt = self.prompts['completeness_check'].format(
            license_type=application_data.get('license_type', 'General'),
            application_data=json.dumps(application_data, indent=2)
        )
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=self.max_tokens,
            temperature=self.temperature
        )
        
        return self._parse_json_response(response.choices[0].message.content)
    
    def _assess_risk(self, application_data: Dict[str, Any]) -> Dict[str, Any]:
        """Assess application risk using structured prompt pattern"""
        prompt = self.prompts['risk_assessment'].format(
            application_data=json.dumps(application_data, indent=2)
        )
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=self.max_tokens,
            temperature=self.temperature
        )
        
        return self._parse_json_response(response.choices[0].message.content)
    
    def _generate_recommendation(self, completeness: Dict, risk: Dict) -> Dict[str, Any]:
        """Generate final recommendation using structured prompt pattern"""
        prompt = self.prompts['final_recommendation'].format(
            completeness_result=json.dumps(completeness, indent=2),
            risk_result=json.dumps(risk, indent=2)
        )
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=self.max_tokens,
            temperature=self.temperature
        )
        
        return self._parse_json_response(response.choices[0].message.content)
    
    def _parse_json_response(self, response_text: str) -> Dict[str, Any]:
        """Parse JSON response with error handling"""
        try:
            # Extract JSON from response (handle cases where LLM adds extra text)
            start_idx = response_text.find('{')
            end_idx = response_text.rfind('}') + 1
            json_str = response_text[start_idx:end_idx]
            return json.loads(json_str)
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON response: {str(e)}")
            return {"error": "Failed to parse AI response", "raw_response": response_text}
    
    def _save_results(self, results: Dict[str, Any]) -> None:
        """Save processing results to file"""
        os.makedirs('outputs', exist_ok=True)
        filename = f"outputs/processing_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        with open(filename, 'w') as f:
            json.dump(results, f, indent=2)
        
        logger.info(f"Results saved to {filename}")

def load_sample_application() -> Dict[str, Any]:
    """Load a sample application for testing"""
    return {
        "application_id": "TDLR-2024-AC-12345",
        "license_type": "Air Conditioning Contractor",
        "applicant_info": {
            "name": "John Smith",
            "business_name": "Smith HVAC Services",
            "address": "123 Main St, Austin, TX 78701",
            "phone": "(512) 555-0123",
            "email": "john@smithhvac.com"
        },
        "documents_submitted": [
            "Application Form TDLR-AC-001",
            "Proof of Insurance - General Liability $1M",
            "Background Check - Travis County Sheriff",
            "Payment Receipt - $185 Application Fee"
        ],
        "work_experience": {
            "years_experience": 8,
            "previous_employers": ["ABC Cooling", "XYZ Mechanical"],
            "certifications": ["EPA 608 Universal", "NATE Certified"]
        },
        "background_info": {
            "criminal_history": "None reported",
            "license_violations": "None",
            "financial_history": "No bankruptcies or liens"
        }
    }

def main():
    """Main function to demonstrate the application processing system"""
    print("🏛️  Texas TDLR License Application Processing System")
    print("=" * 60)
    print("Demonstrating Advanced Prompt Engineering Techniques\n")
    
    # Initialize processor
    try:
        processor = TDLRApplicationProcessor()
    except Exception as e:
        print(f"❌ Error initializing processor: {str(e)}")
        print("💡 Please check your .env file and OpenAI API key")
        return
    
    # Load sample application
    sample_app = load_sample_application()
    print("📋 Processing Sample Application:")
    print(f"   Application ID: {sample_app['application_id']}")
    print(f"   License Type: {sample_app['license_type']}")
    print(f"   Applicant: {sample_app['applicant_info']['name']}\n")
    
    # Process application
    try:
        print("🔄 Running AI-powered application analysis...")
        results = processor.process_application(sample_app)
        
        print("\n✅ Processing Complete! Results:")
        print("-" * 40)
        
        # Display key results
        completeness = results['completeness_check']
        print(f"📊 Completeness Score: {completeness.get('completeness_score', 'N/A')}/100")
        
        risk = results['risk_assessment']
        print(f"⚠️  Risk Level: {risk.get('risk_level', 'N/A')}")
        
        recommendation = results['final_recommendation']
        print(f"✅ Final Recommendation: {recommendation.get('final_recommendation', 'N/A')}")
        
        print(f"\n💾 Detailed results saved to: outputs/processing_results_*.json")
        print("\n🎯 This demonstrates:")
        print("   • Structured prompt patterns for consistent outputs")
        print("   • Multi-step processing pipeline")
        print("   • JSON-formatted results for easy integration")
        print("   • Error handling and logging")
        print("   • Real-world government workflow automation")
        
    except Exception as e:
        print(f"❌ Error processing application: {str(e)}")
        print("💡 Check your internet connection and API key")

if __name__ == "__main__":
    main()

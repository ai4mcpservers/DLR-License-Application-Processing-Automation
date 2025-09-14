#!/usr/bin/env python3
"""
Test Suite for TDLR Application Processing
Demonstrates testing outputs for consistency and performance
"""

import json
import time
import statistics
from typing import List, Dict, Any
from application_processor import TDLRApplicationProcessor, load_sample_application

class PromptPerformanceTestSuite:
    """Test suite for evaluating prompt consistency and performance"""
    
    def __init__(self):
        self.processor = TDLRApplicationProcessor()
        self.test_cases = self._generate_test_cases()
        self.results = []
    
    def _generate_test_cases(self) -> List[Dict[str, Any]]:
        """Generate diverse test cases for comprehensive testing"""
        base_app = load_sample_application()
        
        test_cases = [
            # Complete application
            {**base_app, "test_name": "complete_application"},
            
            # Missing documents
            {**base_app, 
             "documents_submitted": ["Application Form TDLR-AC-001"],
             "test_name": "missing_documents",
             "expected_completeness": "low"
            },
            
            # High risk applicant
            {**base_app,
             "background_info": {
                 "criminal_history": "Misdemeanor theft 2019",
                 "license_violations": "Previous suspension 2020",
                 "financial_history": "Chapter 7 bankruptcy 2021"
             },
             "test_name": "high_risk_applicant",
             "expected_risk": "high"
            },
            
            # New applicant with minimal experience
            {**base_app,
             "work_experience": {
                 "years_experience": 1,
                 "previous_employers": ["Recent Graduate"],
                 "certifications": ["EPA 608 Core Only"]
             },
             "test_name": "minimal_experience",
             "expected_risk": "medium"
            },
            
            # Excellent applicant
            {**base_app,
             "work_experience": {
                 "years_experience": 15,
                 "previous_employers": ["Major HVAC Corp", "Elite Mechanical"],
                 "certifications": ["EPA 608 Universal", "NATE Certified", "Master Technician"]
             },
             "background_info": {
                 "criminal_history": "None",
                 "license_violations": "None",
                 "financial_history": "Excellent credit, business owner"
             },
             "test_name": "excellent_applicant",
             "expected_completeness": "high",
             "expected_risk": "low"
            }
        ]
        
        return test_cases
    
    def run_consistency_test(self, iterations: int = 3) -> Dict[str, Any]:
        """Test prompt consistency by running same input multiple times"""
        print(f"🔄 Running consistency test ({iterations} iterations)...")
        
        test_case = self.test_cases[0]  # Use complete application
        results = []
        
        for i in range(iterations):
            print(f"   Iteration {i+1}/{iterations}")
            result = self.processor.process_application(test_case)
            results.append(result)
        
        # Analyze consistency
        completeness_scores = [r['completeness_check'].get('completeness_score', 0) for r in results]
        risk_scores = [r['risk_assessment'].get('risk_score', 0) for r in results]
        
        consistency_metrics = {
            "completeness_score_variance": statistics.variance(completeness_scores) if len(completeness_scores) > 1 else 0,
            "risk_score_variance": statistics.variance(risk_scores) if len(risk_scores) > 1 else 0,
            "completeness_scores": completeness_scores,
            "risk_scores": risk_scores,
            "consistency_rating": "High" if statistics.variance(completeness_scores) < 5 else "Medium"
        }
        
        return consistency_metrics
    
    def run_performance_test(self) -> Dict[str, Any]:
        """Test processing performance across different application types"""
        print("⚡ Running performance test...")
        
        performance_metrics = {
            "total_tests": len(self.test_cases),
            "processing_times": [],
            "accuracy_scores": [],
            "test_results": []
        }
        
        for i, test_case in enumerate(self.test_cases):
            print(f"   Processing test case {i+1}: {test_case.get('test_name', 'Unknown')}")
            
            start_time = time.time()
            result = self.processor.process_application(test_case)
            processing_time = time.

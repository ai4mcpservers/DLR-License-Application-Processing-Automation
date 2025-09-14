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
            processing_time = time.time() - start_time
            
            # Validate results against expectations
            accuracy_score = self._validate_test_result(test_case, result)
            
            performance_metrics["processing_times"].append(processing_time)
            performance_metrics["accuracy_scores"].append(accuracy_score)
            performance_metrics["test_results"].append({
                "test_name": test_case.get("test_name"),
                "processing_time": processing_time,
                "accuracy_score": accuracy_score,
                "completeness_score": result["completeness_check"].get("completeness_score"),
                "risk_level": result["risk_assessment"].get("risk_level")
            })
        
        # Calculate summary metrics
        performance_metrics.update({
            "average_processing_time": statistics.mean(performance_metrics["processing_times"]),
            "max_processing_time": max(performance_metrics["processing_times"]),
            "average_accuracy": statistics.mean(performance_metrics["accuracy_scores"]),
            "overall_performance_rating": self._calculate_performance_rating(performance_metrics)
        })
        
        return performance_metrics
    
    def _validate_test_result(self, test_case: Dict, result: Dict) -> float:
        """Validate test results against expected outcomes"""
        accuracy_score = 0.0
        total_checks = 0
        
        # Check completeness expectations
        if "expected_completeness" in test_case:
            total_checks += 1
            completeness_score = result["completeness_check"].get("completeness_score", 0)
            
            if test_case["expected_completeness"] == "high" and completeness_score >= 80:
                accuracy_score += 1
            elif test_case["expected_completeness"] == "low" and completeness_score < 60:
                accuracy_score += 1
        
        # Check risk expectations
        if "expected_risk" in test_case:
            total_checks += 1
            risk_level = result["risk_assessment"].get("risk_level", "").lower()
            
            if test_case["expected_risk"].lower() == risk_level:
                accuracy_score += 1
        
        # Default validation for complete applications
        if total_checks == 0:
            total_checks = 2
            completeness_score = result["completeness_check"].get("completeness_score", 0)
            risk_score = result["risk_assessment"].get("risk_score", 10)
            
            if completeness_score >= 70:  # Reasonable completeness
                accuracy_score += 1
            if risk_score <= 5:  # Reasonable risk for clean application
                accuracy_score += 1
        
        return (accuracy_score / total_checks) * 100 if total_checks > 0 else 0
    
    def _calculate_performance_rating(self, metrics: Dict) -> str:
        """Calculate overall performance rating"""
        avg_time = metrics["average_processing_time"]
        avg_accuracy = metrics["average_accuracy"]
        
        if avg_accuracy >= 90 and avg_time < 5:
            return "Excellent"
        elif avg_accuracy >= 80 and avg_time < 10:
            return "Good"
        elif avg_accuracy >= 70 and avg_time < 15:
            return "Fair"
        else:
            return "Needs Improvement"
    
    def run_full_test_suite(self) -> Dict[str, Any]:
        """Run complete test suite with all metrics"""
        print("🧪 Running Full Test Suite for TDLR Application Processing")
        print("=" * 60)
        
        # Run consistency tests
        consistency_results = self.run_consistency_test()
        
        # Run performance tests
        performance_results = self.run_performance_test()
        
        # Compile comprehensive report
        test_report = {
            "test_summary": {
                "total_test_cases": len(self.test_cases),
                "consistency_rating": consistency_results["consistency_rating"],
                "performance_rating": performance_results["overall_performance_rating"],
                "average_processing_time": f"{performance_results['average_processing_time']:.2f} seconds",
                "average_accuracy": f"{performance_results['average_accuracy']:.1f}%"
            },
            "consistency_metrics": consistency_results,
            "performance_metrics": performance_results,
            "recommendations": self._generate_recommendations(consistency_results, performance_results)
        }
        
        return test_report
    
    def _generate_recommendations(self, consistency: Dict, performance: Dict) -> List[str]:
        """Generate improvement recommendations based on test results"""
        recommendations = []
        
        # Consistency recommendations
        if consistency["consistency_rating"] == "Medium":
            recommendations.append("Consider reducing temperature parameter for more consistent outputs")
            recommendations.append("Add more specific constraints to prompt patterns")
        
        # Performance recommendations
        if performance["average_accuracy"] < 85:
            recommendations.append("Review and refine prompt patterns for better accuracy")
            recommendations.append("Add more diverse training examples to test cases")
        
        if performance["average_processing_time"] > 10:
            recommendations.append("Consider optimizing prompt length to reduce processing time")
            recommendations.append("Implement caching for repeated similar requests")
        
        # Default recommendations
        if not recommendations:
            recommendations.append("Performance is excellent - consider expanding to additional license types")
            recommendations.append("Ready for production deployment with current configuration")
        
        return recommendations

def generate_performance_report(test_results: Dict) -> str:
    """Generate a formatted performance report"""
    report = f"""
# TDLR Application Processing - Performance Report
Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}

## Executive Summary
- **Overall Performance Rating**: {test_results['test_summary']['performance_rating']}
- **Consistency Rating**: {test_results['test_summary']['consistency_rating']}
- **Average Processing Time**: {test_results['test_summary']['average_processing_time']}
- **Average Accuracy**: {test_results['test_summary']['average_accuracy']}

## Detailed Metrics

### Consistency Analysis
- **Completeness Score Variance**: {test_results['consistency_metrics']['completeness_score_variance']:.2f}
- **Risk Score Variance**: {test_results['consistency_metrics']['risk_score_variance']:.2f}
- **Sample Completeness Scores**: {test_results['consistency_metrics']['completeness_scores']}

### Performance Analysis
"""
    
    for result in test_results['performance_metrics']['test_results']:
        report += f"""
**Test Case: {result['test_name']}**
- Processing Time: {result['processing_time']:.2f}s
- Accuracy Score: {result['accuracy_score']:.1f}%
- Completeness Score: {result['completeness_score']}
- Risk Level: {result['risk_level']}
"""
    
    report += f"""
## Recommendations
"""
    for i, rec in enumerate(test_results['recommendations'], 1):
        report += f"{i}. {rec}\n"
    
    return report

def main():
    """Main function to run the test suite"""
    print("🧪 TDLR Application Processing - Test Suite")
    print("=" * 50)
    
    try:
        # Initialize test suite
        test_suite = PromptPerformanceTestSuite()
        
        # Run full test suite
        results = test_suite.run_full_test_suite()
        
        # Display results
        print("\n📊 Test Results Summary:")
        print("-" * 30)
        for key, value in results["test_summary"].items():
            print(f"{key.replace('_', ' ').title()}: {value}")
        
        print("\n💡 Recommendations:")
        for i, rec in enumerate(results["recommendations"], 1):
            print(f"{i}. {rec}")
        
        # Generate and save detailed report
        report = generate_performance_report(results)
        with open("outputs/performance_report.md", "w") as f:
            f.write(report)
        
        print(f"\n📄 Detailed report saved to: outputs/performance_report.md")
        
        # Save raw test data
        with open("outputs/test_results.json", "w") as f:
            json.dump(results, f, indent=2)
        
        print("✅ Test suite completed successfully!")
        
    except Exception as e:
        print(f"❌ Error running test suite: {str(e)}")
        print("💡 Please check your configuration and try again")

if __name__ == "__main__":
    main()

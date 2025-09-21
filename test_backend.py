#!/usr/bin/env python3
"""
Test script to verify backend API endpoints work correctly
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.services import RiskProfilerService
from backend.models import UserAnswers

def test_profile_generation():
    """Test the profile generation with sample answers"""
    print("🧪 Testing Risk Profile Generation...")
    
    service = RiskProfilerService()
    
    # Sample answers that match what the frontend would send
    sample_answers = UserAnswers(
        answer1="I'd hold but feel stressed.",
        answer2="Prefer steady growth, some risk okay.",
        answer3="Down payment in ~3 years."
    )
    
    try:
        result = service.generate_profile(sample_answers)
        print("✅ Profile generation successful!")
        print(f"   Label: {result.label}")
        print(f"   Score: {result.score}")
        print(f"   Timeline: {result.profile.timeline_years} years")
        print(f"   Loss Aversion: {result.profile.loss_aversion}")
        print(f"   Axes: {result.axes}")
        return True
    except Exception as e:
        print(f"❌ Profile generation failed: {e}")
        return False

if __name__ == "__main__":
    success = test_profile_generation()
    if success:
        print("\n✅ Backend services are working correctly!")
        print("You can now start the FastAPI server with: python backend/main.py")
    else:
        print("\n❌ Backend services need debugging.")
        print("Make sure Ollama is running with: ollama serve")
        print("And the risk-profiler model is available: ollama list")
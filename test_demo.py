#!/usr/bin/env python3
"""
Automated test for the AI Research Platform Demo

This script tests the core functionality of the demo without requiring user interaction.
"""

import sys
import os
from pathlib import Path

# Add swarms to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from demo_research_platform import ResearchPlatform, MockLLM, setup_llm

def test_mock_llm():
    """Test the mock LLM functionality"""
    print("🧪 Testing Mock LLM...")
    
    mock_llm = MockLLM("Test-LLM")
    
    # Test different types of prompts
    prompts = [
        "Research climate change impacts",
        "Analyze the data for accuracy",
        "Summarize the key findings",
        "Write a comprehensive report"
    ]
    
    for prompt in prompts:
        response = mock_llm(prompt)
        assert len(response) > 50, f"Response too short for prompt: {prompt}"
        assert "Test-LLM" in response, "LLM name not in response"
    
    print("✅ Mock LLM tests passed")

def test_llm_setup():
    """Test LLM setup with fallback"""
    print("🧪 Testing LLM Setup...")
    
    llm = setup_llm()
    assert llm is not None, "LLM setup failed"
    
    # Test a simple call
    response = llm("Hello, this is a test")
    assert len(response) > 0, "LLM response empty"
    
    print("✅ LLM setup tests passed")

def test_platform_initialization():
    """Test platform initialization"""
    print("🧪 Testing Platform Initialization...")
    
    platform = ResearchPlatform()
    
    # Check all agents are created
    assert platform.researcher is not None, "Researcher not initialized"
    assert platform.fact_checker is not None, "Fact checker not initialized"
    assert platform.analyst is not None, "Analyst not initialized"
    assert platform.writer is not None, "Writer not initialized"
    
    # Check workflows are set up
    assert platform.sequential_workflow is not None, "Sequential workflow not initialized"
    assert platform.concurrent_workflow is not None, "Concurrent workflow not initialized"
    assert platform.swarm_network is not None, "Swarm network not initialized"
    
    print("✅ Platform initialization tests passed")

def test_sequential_workflow():
    """Test sequential research workflow"""
    print("🧪 Testing Sequential Workflow...")
    
    platform = ResearchPlatform()
    
    # Run with a simple test topic
    test_topic = "artificial intelligence applications"
    results = platform.run_sequential_research(test_topic)
    
    assert isinstance(results, dict), "Results should be a dictionary"
    assert len(results) > 0, "Results should not be empty"
    
    # Check for expected result keys
    expected_keys = ['primary_research', 'fact_check', 'analysis', 'final_report']
    for key in expected_keys:
        if key in results:
            assert len(results[key]) > 50, f"{key} result too short"
    
    print("✅ Sequential workflow tests passed")

def test_parallel_workflow():
    """Test parallel analysis workflow"""
    print("🧪 Testing Parallel Workflow...")
    
    platform = ResearchPlatform()
    
    # Run with a simple test topic
    test_topic = "renewable energy trends"
    results = platform.run_parallel_analysis(test_topic)
    
    assert isinstance(results, dict), "Results should be a dictionary"
    assert len(results) > 0, "Results should not be empty"
    
    print("✅ Parallel workflow tests passed")

def test_file_operations():
    """Test file save/load operations"""
    print("🧪 Testing File Operations...")
    
    from demo_research_platform import save_research_data, load_research_data
    
    # Test save
    test_content = "This is test research data for validation."
    test_filename = "test_data.md"
    
    save_result = save_research_data(test_filename, test_content)
    assert "Successfully saved" in save_result, f"Save failed: {save_result}"
    
    # Test load
    load_result = load_research_data(test_filename)
    assert load_result == test_content, "Loaded content doesn't match saved content"
    
    # Cleanup
    test_file = Path("research_output") / test_filename
    if test_file.exists():
        test_file.unlink()
    
    print("✅ File operations tests passed")

def test_tools():
    """Test tool functionality"""
    print("🧪 Testing Tools...")
    
    from demo_research_platform import search_web
    
    # Test web search tool (mock)
    search_result = search_web("test query")
    assert len(search_result) > 50, "Search result too short"
    assert "Web Search Results" in search_result, "Search format incorrect"
    
    print("✅ Tools tests passed")

def run_comprehensive_test():
    """Run all tests"""
    print("🚀 Starting Comprehensive Demo Tests")
    print("=" * 50)
    
    try:
        test_mock_llm()
        test_llm_setup()
        test_platform_initialization()
        test_file_operations()
        test_tools()
        test_sequential_workflow()
        test_parallel_workflow()
        
        print("\n" + "=" * 50)
        print("🎉 ALL TESTS PASSED! 🎉")
        print("✅ The AI Research Platform Demo is fully functional")
        print("🚀 Ready for interactive demonstration")
        
        # Show quick demo
        print("\n" + "=" * 50)
        print("📋 QUICK DEMO PREVIEW")
        print("=" * 50)
        
        platform = ResearchPlatform()
        sample_results = platform.run_sequential_research("machine learning trends")
        
        print("\n🔬 Sample Research Results:")
        for key, value in sample_results.items():
            if key != 'error':
                preview = str(value)[:200] + "..." if len(str(value)) > 200 else str(value)
                print(f"\n📋 {key.upper().replace('_', ' ')}:")
                print(f"   {preview}")
        
        return True
        
    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        print("Please check the error and fix any issues before running the demo")
        return False

if __name__ == "__main__":
    success = run_comprehensive_test()
    sys.exit(0 if success else 1)
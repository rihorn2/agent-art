#!/usr/bin/env python3
"""
Simple test script for the Mathematical Visualization Generator
"""

import os
import sys
import subprocess

def test_basic_functionality():
    """Test basic functionality of the matvis_simple.py script."""
    print("Testing Mathematical Visualization Generator...")
    
    # Test cases
    test_cases = [
        ("plot f(x) = x^2", "test_quadratic"),
        ("show a circle", "test_circle"), 
        ("derivative of x squared", "test_derivative"),
        ("sine wave", "test_sine"),
    ]
    
    success_count = 0
    
    for description, filename in test_cases:
        print(f"\n🧪 Testing: {description}")
        
        try:
            result = subprocess.run([
                sys.executable, "matvis_simple.py", description, "-o", filename
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                output_file = f"output/{filename}.svg"
                if os.path.exists(output_file):
                    print(f"✅ SUCCESS: {output_file} created")
                    success_count += 1
                else:
                    print(f"❌ FAIL: {output_file} not found")
            else:
                print(f"❌ FAIL: Command failed with exit code {result.returncode}")
                print(f"Error: {result.stderr}")
                
        except Exception as e:
            print(f"❌ FAIL: Exception occurred: {e}")
    
    print(f"\n📊 Test Results: {success_count}/{len(test_cases)} tests passed")
    
    if success_count == len(test_cases):
        print("🎉 All tests passed! The application is working correctly.")
        return True
    else:
        print("⚠️  Some tests failed. Check the errors above.")
        return False

if __name__ == "__main__":
    test_basic_functionality()
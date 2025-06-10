#!/usr/bin/env python3
"""
Example usage of the Simple Mathematical Visualization Generator

This script demonstrates the working version that generates SVG visualizations.
"""

import subprocess
import sys
import os

def run_example(description, output_name):
    """Run a single example and show the command."""
    print(f"\n🔹 Example: {description}")
    print(f"Command: python matvis_simple.py \"{description}\" -o {output_name}")
    
    try:
        result = subprocess.run([
            sys.executable, "matvis_simple.py", description, "-o", output_name
        ], capture_output=True, text=True, cwd=os.path.dirname(__file__))
        
        if result.returncode == 0:
            print("✅ Success!")
            print(result.stdout)
        else:
            print("❌ Error:")
            print(result.stderr)
    except Exception as e:
        print(f"❌ Exception: {e}")

def main():
    """Run various examples of the mathematical visualization generator."""
    print("Mathematical Visualization Generator - Simple SVG Examples")
    print("=" * 60)
    
    examples = [
        ("plot the function f(x) = x^2", "quadratic_function"),
        ("show a sine wave y = sin(x)", "sine_wave"),
        ("demonstrate a circle with radius r", "circle_geometry"),
        ("show the derivative of x squared", "derivative_example"),
        ("plot the integral of x^2 from -1 to 1", "integral_example"),
        ("show a triangle with labeled vertices", "triangle_geometry"),
        ("graph y = cos(x)", "cosine_wave"),
        ("show a parabola", "parabola"),
    ]
    
    for description, output_name in examples:
        run_example(description, output_name)
    
    print("\n" + "=" * 60)
    print("Examples completed! Check the 'output' directory for generated SVG files.")
    print("💡 You can open any .svg file in a web browser to view the visualizations")

if __name__ == "__main__":
    main()
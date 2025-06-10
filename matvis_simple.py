#!/usr/bin/env python3
"""
Simple Mathematical Visualization Generator (Demo Version)

This is a simplified demonstration version that shows the concept without
external dependencies. It creates SVG files instead of requiring matplotlib.
"""

import click
import os
import re
import math
from typing import List, Dict, Any


class MathVisualizationGenerator:
    """Simple demonstration class for generating mathematical visualizations."""
    
    def __init__(self):
        self.output_dir = "output"
        self.width = 800
        self.height = 600
        
    def parse_description(self, description: str) -> Dict[str, Any]:
        """Parse the input description to extract mathematical concepts."""
        parsed = {
            'functions': [],
            'equations': [],
            'concepts': [],
            'animation_type': 'basic',
            'description': description.lower()
        }
        
        # Look for function patterns
        function_patterns = [
            r'f\(x\)\s*=\s*([^,\.]+)',
            r'y\s*=\s*([^,\.]+)',
        ]
        
        for pattern in function_patterns:
            matches = re.findall(pattern, description, re.IGNORECASE)
            parsed['functions'].extend(matches)
        
        # Identify mathematical concepts
        concept_keywords = {
            'derivative': ['derivative', 'differentiation', 'slope', 'tangent'],
            'integral': ['integral', 'integration', 'area under curve'],
            'trigonometry': ['sin', 'cos', 'tan', 'sine', 'cosine', 'tangent'],
            'quadratic': ['quadratic', 'parabola', 'x^2', 'x squared'],
            'linear': ['linear', 'line', 'straight'],
            'exponential': ['exponential', 'e^x', 'exp'],
            'circle': ['circle', 'circumference', 'radius'],
            'geometry': ['triangle', 'square', 'rectangle', 'polygon']
        }
        
        for concept, keywords in concept_keywords.items():
            if any(keyword in description.lower() for keyword in keywords):
                parsed['concepts'].append(concept)
        
        return parsed
    
    def create_svg_header(self, width: int, height: int) -> str:
        """Create SVG header."""
        return f'''<?xml version="1.0" encoding="UTF-8"?>
<svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg">
<rect width="100%" height="100%" fill="white"/>
'''

    def create_svg_footer(self) -> str:
        """Create SVG footer."""
        return '</svg>'
    
    def draw_axes(self, cx: int, cy: int, scale: int = 40) -> str:
        """Draw coordinate axes."""
        svg = f'''
<!-- Axes -->
<line x1="50" y1="{cy}" x2="{self.width-50}" y2="{cy}" stroke="black" stroke-width="2"/>
<line x1="{cx}" y1="50" x2="{cx}" y2="{self.height-50}" stroke="black" stroke-width="2"/>

<!-- Grid -->
'''
        # Add grid lines
        for i in range(-10, 11):
            if i != 0:
                x = cx + i * scale
                y = cy + i * scale
                if 50 <= x <= self.width - 50:
                    svg += f'<line x1="{x}" y1="50" x2="{x}" y2="{self.height-50}" stroke="lightgray" stroke-width="1"/>\n'
                if 50 <= y <= self.height - 50:
                    svg += f'<line x1="50" y1="{y}" x2="{self.width-50}" y2="{y}" stroke="lightgray" stroke-width="1"/>\n'
        
        # Add axis labels
        svg += f'''
<text x="{self.width-30}" y="{cy+20}" font-family="Arial" font-size="14">x</text>
<text x="{cx-15}" y="40" font-family="Arial" font-size="14">y</text>
'''
        return svg
    
    def plot_quadratic(self, cx: int, cy: int, scale: int = 40) -> str:
        """Plot a quadratic function y = x^2."""
        svg = ''
        points = []
        
        for i in range(-200, 201, 5):
            x_val = i / 40.0  # Scale to reasonable range
            y_val = x_val * x_val
            
            x_pixel = cx + x_val * scale
            y_pixel = cy - y_val * scale  # Flip y-axis
            
            if 50 <= x_pixel <= self.width - 50 and 50 <= y_pixel <= self.height - 50:
                points.append(f"{x_pixel},{y_pixel}")
        
        if points:
            svg += f'<polyline points="{" ".join(points)}" fill="none" stroke="blue" stroke-width="3"/>\n'
            svg += f'<text x="100" y="100" font-family="Arial" font-size="16" fill="blue">f(x) = x²</text>\n'
        
        return svg
    
    def plot_sine(self, cx: int, cy: int, scale: int = 40) -> str:
        """Plot a sine function y = sin(x)."""
        svg = ''
        points = []
        
        for i in range(-628, 629, 5):  # -2π to 2π
            x_val = i / 100.0
            y_val = math.sin(x_val)
            
            x_pixel = cx + x_val * scale
            y_pixel = cy - y_val * scale
            
            if 50 <= x_pixel <= self.width - 50 and 50 <= y_pixel <= self.height - 50:
                points.append(f"{x_pixel},{y_pixel}")
        
        if points:
            svg += f'<polyline points="{" ".join(points)}" fill="none" stroke="red" stroke-width="3"/>\n'
            svg += f'<text x="100" y="100" font-family="Arial" font-size="16" fill="red">f(x) = sin(x)</text>\n'
        
        return svg
    
    def draw_circle(self, cx: int, cy: int, radius: int = 100) -> str:
        """Draw a circle with radius annotation."""
        svg = f'''
<circle cx="{cx}" cy="{cy}" r="{radius}" fill="lightblue" fill-opacity="0.3" stroke="blue" stroke-width="3"/>
<line x1="{cx}" y1="{cy}" x2="{cx + radius}" y2="{cy}" stroke="red" stroke-width="2"/>
<circle cx="{cx}" cy="{cy}" r="3" fill="black"/>
<circle cx="{cx + radius}" cy="{cy}" r="3" fill="red"/>
<text x="{cx + radius//2}" y="{cy - 10}" font-family="Arial" font-size="14" text-anchor="middle">r</text>
<text x="{cx}" y="{cy + radius + 30}" font-family="Arial" font-size="16" text-anchor="middle">Circle: C = 2πr, A = πr²</text>
'''
        return svg
    
    def draw_triangle(self, cx: int, cy: int) -> str:
        """Draw a triangle with labeled vertices."""
        # Triangle vertices
        x1, y1 = cx - 100, cy + 80
        x2, y2 = cx + 100, cy + 80
        x3, y3 = cx, cy - 100
        
        svg = f'''
<polygon points="{x1},{y1} {x2},{y2} {x3},{y3}" fill="lightgreen" fill-opacity="0.3" stroke="green" stroke-width="3"/>
<circle cx="{x1}" cy="{y1}" r="3" fill="black"/>
<circle cx="{x2}" cy="{y2}" r="3" fill="black"/>
<circle cx="{x3}" cy="{y3}" r="3" fill="black"/>
<text x="{x1-15}" y="{y1+20}" font-family="Arial" font-size="14" font-weight="bold">A</text>
<text x="{x2+10}" y="{y2+20}" font-family="Arial" font-size="14" font-weight="bold">B</text>
<text x="{x3}" y="{y3-10}" font-family="Arial" font-size="14" font-weight="bold" text-anchor="middle">C</text>
<text x="{cx}" y="{cy + 120}" font-family="Arial" font-size="16" text-anchor="middle">Triangle: A = ½ × base × height</text>
'''
        return svg
    
    def create_function_plot(self, functions: List[str], title: str) -> str:
        """Create an SVG plot of mathematical functions."""
        cx, cy = self.width // 2, self.height // 2
        scale = 40
        
        svg = self.create_svg_header(self.width, self.height)
        svg += f'<text x="{self.width//2}" y="30" font-family="Arial" font-size="20" font-weight="bold" text-anchor="middle">{title}</text>\n'
        svg += self.draw_axes(cx, cy, scale)
        
        # Plot functions based on description
        plotted = False
        for func_str in functions:
            if isinstance(func_str, tuple):
                func_str = func_str[0] if len(func_str) > 0 else func_str[1]
            
            if 'x^2' in func_str or 'x**2' in func_str or 'squared' in func_str:
                svg += self.plot_quadratic(cx, cy, scale)
                plotted = True
            elif 'sin' in func_str:
                svg += self.plot_sine(cx, cy, scale)
                plotted = True
        
        # Default to quadratic if nothing was plotted
        if not plotted:
            svg += self.plot_quadratic(cx, cy, scale)
        
        svg += self.create_svg_footer()
        return svg
    
    def create_geometry_plot(self, concepts: List[str], title: str) -> str:
        """Create an SVG plot of geometric shapes."""
        cx, cy = self.width // 2, self.height // 2
        
        svg = self.create_svg_header(self.width, self.height)
        svg += f'<text x="{self.width//2}" y="30" font-family="Arial" font-size="20" font-weight="bold" text-anchor="middle">{title}</text>\n'
        
        if 'circle' in concepts:
            svg += self.draw_circle(cx, cy)
        elif 'triangle' in concepts:
            svg += self.draw_triangle(cx, cy)
        else:
            # Default: show a circle
            svg += self.draw_circle(cx, cy)
        
        svg += self.create_svg_footer()
        return svg
    
    def create_calculus_plot(self, concepts: List[str], title: str) -> str:
        """Create an SVG plot showing calculus concepts."""
        cx, cy = self.width // 2, self.height // 2
        scale = 40
        
        svg = self.create_svg_header(self.width, self.height)
        svg += f'<text x="{self.width//2}" y="30" font-family="Arial" font-size="20" font-weight="bold" text-anchor="middle">{title}</text>\n'
        svg += self.draw_axes(cx, cy, scale)
        
        # Draw parabola
        svg += self.plot_quadratic(cx, cy, scale)
        
        if 'derivative' in concepts:
            # Show tangent line at x=1
            x_val = 1
            y_val = x_val * x_val
            slope = 2 * x_val  # derivative of x^2 is 2x
            
            x_pixel = cx + x_val * scale
            y_pixel = cy - y_val * scale
            
            # Tangent line points
            x1 = x_pixel - 40
            y1 = y_pixel + slope * 40
            x2 = x_pixel + 40
            y2 = y_pixel - slope * 40
            
            svg += f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="red" stroke-width="2"/>\n'
            svg += f'<circle cx="{x_pixel}" cy="{y_pixel}" r="4" fill="red"/>\n'
            svg += f'<text x="100" y="130" font-family="Arial" font-size="14" fill="red">Tangent line (slope = {slope})</text>\n'
            svg += f'<text x="100" y="150" font-family="Arial" font-size="14">Derivative: f\'(x) = 2x</text>\n'
        
        elif 'integral' in concepts:
            # Show area under curve from -1 to 1
            svg += f'<text x="100" y="130" font-family="Arial" font-size="14" fill="orange">Area under curve</text>\n'
            svg += f'<text x="100" y="150" font-family="Arial" font-size="14">Integral: ∫x²dx</text>\n'
            
            # Add shaded area (simplified)
            x1 = cx - scale
            x2 = cx + scale
            svg += f'<rect x="{x1}" y="{cy}" width="{2*scale}" height="{scale}" fill="yellow" fill-opacity="0.3"/>\n'
        
        svg += self.create_svg_footer()
        return svg
    
    def generate_visualization(self, description: str, output_file: str = None) -> str:
        """Generate an SVG visualization from a text description."""
        parsed = self.parse_description(description)
        
        # Create output directory
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Determine which type of visualization to create
        if parsed['functions']:
            svg_content = self.create_function_plot(parsed['functions'], f"Functions: {description}")
        elif 'geometry' in parsed['concepts'] or any(geo in parsed['concepts'] for geo in ['circle', 'triangle']):
            svg_content = self.create_geometry_plot(parsed['concepts'], f"Geometry: {description}")
        elif any(calc in parsed['concepts'] for calc in ['derivative', 'integral']):
            svg_content = self.create_calculus_plot(parsed['concepts'], f"Calculus: {description}")
        else:
            # Default to basic function visualization
            svg_content = self.create_function_plot(['x^2'], f"Default: {description}")
        
        # Generate output filename
        if output_file is None:
            output_file = "math_visualization"
        
        output_path = f"{self.output_dir}/{output_file}.svg"
        
        # Save the SVG file
        with open(output_path, 'w') as f:
            f.write(svg_content)
        
        return output_path


@click.command()
@click.argument('description')
@click.option('--output', '-o', default=None, help='Output filename (without extension)')
@click.option('--output-dir', default='output', help='Output directory')
def main(description: str, output: str, output_dir: str):
    """
    Generate mathematical visualization SVG files from text descriptions.
    
    DESCRIPTION: Text description of the mathematical concept to visualize
    
    Examples:
    
    python matvis_simple.py "plot the function f(x) = x^2"
    
    python matvis_simple.py "show a circle with radius r"
    
    python matvis_simple.py "demonstrate the derivative of x squared"
    """
    generator = MathVisualizationGenerator()
    generator.output_dir = output_dir
    
    print(f"Generating visualization for: {description}")
    
    try:
        output_path = generator.generate_visualization(description, output)
        if output_path:
            print(f"✅ SVG generated successfully: {output_path}")
            print(f"💡 Open the file in a web browser to view the visualization")
        else:
            print("❌ Failed to generate SVG")
    except Exception as e:
        print(f"❌ Error generating visualization: {e}")


if __name__ == "__main__":
    main()
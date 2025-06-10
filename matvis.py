#!/usr/bin/env python3
"""
Mathematical Visualization Generator using Matplotlib

This application takes string descriptions and generates mathematical static visualizations
using the Matplotlib library. Can be extended to use Manim for animations.
"""

import click
import os
import re
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from typing import List, Dict, Any
import math


class MathVisualizationGenerator:
    """Main class for generating mathematical visualizations from text descriptions."""
    
    def __init__(self):
        self.output_dir = "output"
        self.figure_size = (10, 8)
        
    def parse_description(self, description: str) -> Dict[str, Any]:
        """
        Parse the input description to extract mathematical concepts and visualization hints.
        
        Args:
            description: String description of the mathematical concept to visualize
            
        Returns:
            Dictionary containing parsed elements like functions, equations, concepts, etc.
        """
        parsed = {
            'functions': [],
            'equations': [],
            'concepts': [],
            'animation_type': 'basic',
            'description': description.lower()
        }
        
        # Look for function patterns like f(x) = x^2, y = sin(x), etc.
        function_patterns = [
            r'f\(x\)\s*=\s*([^,\.]+)',
            r'y\s*=\s*([^,\.]+)',
            r'([a-z]+)\(x\)\s*=\s*([^,\.]+)'
        ]
        
        for pattern in function_patterns:
            matches = re.findall(pattern, description, re.IGNORECASE)
            parsed['functions'].extend(matches)
        
        # Look for equation patterns
        equation_patterns = [
            r'(\w+\s*[\+\-\*/\^]\s*\w+\s*=\s*\w+)',
            r'(x\^2\s*\+\s*y\^2\s*=\s*\d+)',  # Circle equations
        ]
        
        for pattern in equation_patterns:
            matches = re.findall(pattern, description, re.IGNORECASE)
            parsed['equations'].extend(matches)
        
        # Identify mathematical concepts
        concept_keywords = {
            'derivative': ['derivative', 'differentiation', 'slope', 'tangent'],
            'integral': ['integral', 'integration', 'area under curve'],
            'limit': ['limit', 'approaching', 'tends to'],
            'trigonometry': ['sin', 'cos', 'tan', 'sine', 'cosine', 'tangent'],
            'quadratic': ['quadratic', 'parabola', 'x^2', 'x squared'],
            'linear': ['linear', 'line', 'straight'],
            'exponential': ['exponential', 'e^x', 'exp'],
            'logarithm': ['log', 'logarithm', 'ln'],
            'circle': ['circle', 'circumference', 'radius'],
            'geometry': ['triangle', 'square', 'rectangle', 'polygon']
        }
        
        for concept, keywords in concept_keywords.items():
            if any(keyword in description.lower() for keyword in keywords):
                parsed['concepts'].append(concept)
        
        # Determine visualization type based on content
        if any(word in description.lower() for word in ['graph', 'plot', 'function']):
            parsed['animation_type'] = 'graph'
        elif any(word in description.lower() for word in ['geometry', 'shape', 'triangle', 'circle']):
            parsed['animation_type'] = 'geometry'
        elif any(word in description.lower() for word in ['derivative', 'integral', 'calculus']):
            parsed['animation_type'] = 'calculus'
            
        return parsed
    
    def plot_basic_functions(self, functions: List[str], title: str = "Mathematical Functions") -> plt.Figure:
        """Create a plot showing basic mathematical functions."""
        
        fig, ax = plt.subplots(figsize=self.figure_size)
        
        # Set up the plot
        x = np.linspace(-5, 5, 1000)
        
        colors = ['blue', 'red', 'green', 'orange', 'purple', 'brown']
        color_idx = 0
        
        # Plot functions
        for func_str in functions:
            try:
                # Handle tuple format from regex
                if isinstance(func_str, tuple):
                    func_str = func_str[0] if len(func_str) > 0 else func_str[1]
                
                # Create function from string (basic cases)
                if 'x^2' in func_str or 'x**2' in func_str:
                    y = x**2
                    label = 'f(x) = x²'
                elif 'sin' in func_str:
                    y = np.sin(x)
                    label = 'f(x) = sin(x)'
                elif 'cos' in func_str:
                    y = np.cos(x)
                    label = 'f(x) = cos(x)'
                elif 'x^3' in func_str or 'x**3' in func_str:
                    y = x**3
                    label = 'f(x) = x³'
                elif 'exp' in func_str or 'e^x' in func_str:
                    y = np.exp(x)
                    label = 'f(x) = eˣ'
                    # Limit y range for exponential
                    mask = y < 50
                    x_plot, y_plot = x[mask], y[mask]
                    ax.plot(x_plot, y_plot, color=colors[color_idx % len(colors)], linewidth=2, label=label)
                    color_idx += 1
                    continue
                elif 'log' in func_str or 'ln' in func_str:
                    # Only plot for positive x values
                    x_pos = x[x > 0.1]
                    y = np.log(x_pos)
                    ax.plot(x_pos, y, color=colors[color_idx % len(colors)], linewidth=2, label='f(x) = ln(x)')
                    color_idx += 1
                    continue
                else:
                    # Default to linear function
                    y = x
                    label = 'f(x) = x'
                
                # Plot the function
                ax.plot(x, y, color=colors[color_idx % len(colors)], linewidth=2, label=label)
                color_idx += 1
                
            except Exception as e:
                print(f"Could not parse function: {func_str}, error: {e}")
                continue
        
        # If no functions were plotted, plot a default one
        if color_idx == 0:
            y = x**2
            ax.plot(x, y, color='blue', linewidth=2, label='f(x) = x²')
        
        # Set up the plot appearance
        ax.grid(True, alpha=0.3)
        ax.axhline(y=0, color='black', linewidth=0.5)
        ax.axvline(x=0, color='black', linewidth=0.5)
        ax.set_xlabel('x', fontsize=12)
        ax.set_ylabel('y', fontsize=12)
        ax.set_title(title, fontsize=14, fontweight='bold')
        ax.legend()
        
        # Set reasonable limits
        ax.set_ylim(-10, 10)
        
        plt.tight_layout()
        return fig
    
    def plot_geometry(self, concepts: List[str], title: str = "Geometric Shapes") -> plt.Figure:
        """Create a plot showing geometric shapes and their properties."""
        
        fig, ax = plt.subplots(figsize=self.figure_size)
        
        if 'circle' in concepts:
            # Draw a circle
            circle = patches.Circle((0, 0), 2, linewidth=2, edgecolor='blue', facecolor='lightblue', alpha=0.5)
            ax.add_patch(circle)
            
            # Add radius line
            ax.plot([0, 2], [0, 0], 'r-', linewidth=2, label='radius = r')
            ax.plot(0, 0, 'ko', markersize=5)  # Center point
            ax.plot(2, 0, 'ro', markersize=5)  # Point on circumference
            
            # Add annotations
            ax.annotate('Center', xy=(0, 0), xytext=(0.3, 0.3), fontsize=10)
            ax.annotate('r', xy=(1, 0), xytext=(1, -0.3), fontsize=12, ha='center')
            
            # Add formula
            ax.text(0, -3.5, 'Circumference: C = 2πr\nArea: A = πr²', 
                   fontsize=12, ha='center', bbox=dict(boxstyle="round,pad=0.3", facecolor="wheat"))
            
            ax.set_xlim(-3, 3)
            ax.set_ylim(-4, 3)
            
        elif 'triangle' in concepts:
            # Draw a triangle
            triangle_points = np.array([[-2, -1], [2, -1], [0, 2], [-2, -1]])
            ax.plot(triangle_points[:, 0], triangle_points[:, 1], 'g-', linewidth=2)
            triangle = patches.Polygon(triangle_points[:-1], closed=True, 
                                     linewidth=2, edgecolor='green', facecolor='lightgreen', alpha=0.5)
            ax.add_patch(triangle)
            
            # Label vertices
            ax.annotate('A', xy=(-2, -1), xytext=(-2.3, -1.3), fontsize=12, fontweight='bold')
            ax.annotate('B', xy=(2, -1), xytext=(2.2, -1.3), fontsize=12, fontweight='bold')
            ax.annotate('C', xy=(0, 2), xytext=(0.2, 2.2), fontsize=12, fontweight='bold')
            
            # Add formula
            ax.text(0, -2.5, 'Area: A = ½ × base × height', 
                   fontsize=12, ha='center', bbox=dict(boxstyle="round,pad=0.3", facecolor="wheat"))
            
            ax.set_xlim(-3, 3)
            ax.set_ylim(-3, 3)
        
        else:
            # Default: show multiple basic shapes
            # Circle
            circle = patches.Circle((-1.5, 1), 0.8, linewidth=2, edgecolor='blue', facecolor='lightblue', alpha=0.5)
            ax.add_patch(circle)
            ax.text(-1.5, 0, 'Circle', ha='center', fontsize=10)
            
            # Square
            square = patches.Rectangle((0.5, 0.5), 1, 1, linewidth=2, edgecolor='red', facecolor='lightcoral', alpha=0.5)
            ax.add_patch(square)
            ax.text(1, 0, 'Square', ha='center', fontsize=10)
            
            # Triangle
            triangle = patches.Polygon([[-1, -1], [0, -1], [-0.5, -0.2]], closed=True,
                                     linewidth=2, edgecolor='green', facecolor='lightgreen', alpha=0.5)
            ax.add_patch(triangle)
            ax.text(-0.5, -1.5, 'Triangle', ha='center', fontsize=10)
            
            ax.set_xlim(-3, 3)
            ax.set_ylim(-2, 2.5)
        
        ax.set_aspect('equal')
        ax.grid(True, alpha=0.3)
        ax.set_xlabel('x', fontsize=12)
        ax.set_ylabel('y', fontsize=12)
        ax.set_title(title, fontsize=14, fontweight='bold')
        
        plt.tight_layout()
        return fig
    
    def plot_calculus_concepts(self, concepts: List[str], title: str = "Calculus Concepts") -> plt.Figure:
        """Create a plot showing calculus concepts like derivatives and integrals."""
        
        fig, ax = plt.subplots(figsize=self.figure_size)
        
        # Set up basic function (parabola)
        x = np.linspace(-3, 3, 1000)
        y = x**2
        
        ax.plot(x, y, 'b-', linewidth=2, label='f(x) = x²')
        
        if 'derivative' in concepts:
            # Show tangent line at x=1 (derivative demonstration)
            x_point = 1
            y_point = x_point**2
            
            # Derivative of x^2 is 2x, so slope at x=1 is 2
            slope = 2 * x_point
            
            # Create tangent line
            x_tangent = np.linspace(x_point - 1, x_point + 1, 100)
            y_tangent = slope * (x_tangent - x_point) + y_point
            
            ax.plot(x_tangent, y_tangent, 'r-', linewidth=2, label=f'Tangent line (slope = {slope})')
            ax.plot(x_point, y_point, 'ro', markersize=8, label=f'Point ({x_point}, {y_point})')
            
            # Add annotation
            ax.annotate(f'f\'({x_point}) = {slope}', 
                       xy=(x_point, y_point), xytext=(x_point + 0.5, y_point + 1),
                       arrowprops=dict(arrowstyle='->', color='red'),
                       fontsize=12, color='red')
            
            # Add derivative formula
            ax.text(-2.5, 7, 'Derivative: f\'(x) = 2x\nSlope of tangent line', 
                   fontsize=11, bbox=dict(boxstyle="round,pad=0.3", facecolor="lightyellow"))
        
        elif 'integral' in concepts:
            # Show area under curve (integral demonstration)
            x_fill = np.linspace(-1, 1, 100)
            y_fill = x_fill**2
            
            ax.fill_between(x_fill, y_fill, alpha=0.3, color='yellow', label='Area under curve')
            
            # Add vertical lines at bounds
            ax.axvline(x=-1, color='orange', linestyle='--', alpha=0.7)
            ax.axvline(x=1, color='orange', linestyle='--', alpha=0.7)
            
            # Calculate and display the integral value
            integral_value = (1**3 - (-1)**3) / 3  # ∫x²dx from -1 to 1 = x³/3
            
            ax.text(-2.5, 7, f'Integral: ∫x²dx from -1 to 1\nArea = {integral_value:.3f}', 
                   fontsize=11, bbox=dict(boxstyle="round,pad=0.3", facecolor="lightyellow"))
        
        else:
            # Default: show both concepts
            # Derivative at x=1
            x_point = 1
            y_point = x_point**2
            slope = 2 * x_point
            x_tangent = np.linspace(x_point - 0.8, x_point + 0.8, 100)
            y_tangent = slope * (x_tangent - x_point) + y_point
            ax.plot(x_tangent, y_tangent, 'r-', linewidth=2, alpha=0.7, label='Derivative (tangent)')
            ax.plot(x_point, y_point, 'ro', markersize=6)
            
            # Integral from 0 to 2
            x_fill = np.linspace(0, 2, 100)
            y_fill = x_fill**2
            ax.fill_between(x_fill, y_fill, alpha=0.3, color='yellow', label='Integral (area)')
        
        ax.grid(True, alpha=0.3)
        ax.axhline(y=0, color='black', linewidth=0.5)
        ax.axvline(x=0, color='black', linewidth=0.5)
        ax.set_xlabel('x', fontsize=12)
        ax.set_ylabel('y', fontsize=12)
        ax.set_title(title, fontsize=14, fontweight='bold')
        ax.legend()
        ax.set_ylim(-1, 8)
        
        plt.tight_layout()
        return fig
    
    def generate_visualization(self, description: str, output_file: str = None) -> str:
        """
        Generate a mathematical visualization image from a text description.
        
        Args:
            description: Text description of the mathematical concept
            output_file: Optional output filename (without extension)
            
        Returns:
            Path to the generated image file
        """
        parsed = self.parse_description(description)
        
        # Create output directory
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Determine which type of visualization to create
        if parsed['functions']:
            fig = self.plot_basic_functions(parsed['functions'], f"Functions: {description}")
        elif 'geometry' in parsed['concepts'] or any(geo in parsed['concepts'] for geo in ['circle', 'triangle']):
            fig = self.plot_geometry(parsed['concepts'], f"Geometry: {description}")
        elif any(calc in parsed['concepts'] for calc in ['derivative', 'integral', 'limit']):
            fig = self.plot_calculus_concepts(parsed['concepts'], f"Calculus: {description}")
        else:
            # Default to basic function visualization
            fig = self.plot_basic_functions(['x^2'], f"Default: {description}")
        
        # Generate output filename
        if output_file is None:
            output_file = "math_visualization"
        
        output_path = f"{self.output_dir}/{output_file}.png"
        
        # Save the figure
        fig.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close(fig)
        
        return output_path


@click.command()
@click.argument('description')
@click.option('--output', '-o', default=None, help='Output filename (without extension)')
@click.option('--output-dir', default='output', help='Output directory')
def main(description: str, output: str, output_dir: str):
    """
    Generate mathematical visualization images from text descriptions.
    
    DESCRIPTION: Text description of the mathematical concept to visualize
    
    Examples:
    
    python matvis.py "plot the function f(x) = x^2"
    
    python matvis.py "show a circle with radius r and its circumference formula"
    
    python matvis.py "demonstrate the derivative of x squared"
    """
    generator = MathVisualizationGenerator()
    generator.output_dir = output_dir
    
    print(f"Generating visualization for: {description}")
    
    try:
        output_path = generator.generate_visualization(description, output)
        if output_path:
            print(f"✅ Image generated successfully: {output_path}")
        else:
            print("❌ Failed to generate image")
    except Exception as e:
        print(f"❌ Error generating visualization: {e}")


if __name__ == "__main__":
    main()
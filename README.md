# Mathematical Visualization Generator

This application takes string descriptions and generates mathematical visualizations. It currently includes a working SVG-based implementation and a more advanced Matplotlib-based version.

## Features

- Parse natural language descriptions of mathematical concepts
- Generate visualizations showing:
  - Function plots (quadratic, trigonometric, exponential, etc.)
  - Geometric shapes and their properties
  - Calculus concepts (derivatives, integrals)
  - Mathematical transformations

## Quick Start

The simplest way to get started is with the SVG-based version that has no external dependencies:

```bash
# Generate a quadratic function visualization
python matvis_simple.py "plot the function f(x) = x^2" -o quadratic

# Generate a circle with radius
python matvis_simple.py "show a circle with radius r" -o circle

# Generate a derivative visualization
python matvis_simple.py "demonstrate the derivative of x squared" -o derivative
```

## Installation

### Simple SVG Version (No Dependencies)

The `matvis_simple.py` script works out of the box with just Python 3:

```bash
python matvis_simple.py "your description here"
```

### Advanced Matplotlib Version

For higher quality static images, install the dependencies:

```bash
pip install -r requirements.txt
python matvis.py "your description here"
```

## Usage

### Command Line Interface

```bash
# Basic usage (SVG version)
python matvis_simple.py "plot the function f(x) = x^2"

# Specify output filename
python matvis_simple.py "show a sine wave" -o sine_example

# Specify output directory
python matvis_simple.py "demonstrate the derivative of x squared" --output-dir ./images
```

### Examples

Run the examples script to see various demonstrations:

```bash
# SVG examples (no dependencies required)
python examples_simple.py

# Matplotlib examples (requires dependencies)
python examples.py
```

### Supported Descriptions

The application can parse and visualize:

#### Functions
- `"plot the function f(x) = x^2"`
- `"show a sine wave y = sin(x)"`
- `"graph y = cos(x)"`
- `"plot f(x) = x^3"`

#### Geometry
- `"show a circle with radius r"`
- `"demonstrate a triangle with labeled vertices"`
- `"display a square with side length s"`

#### Calculus
- `"show the derivative of x squared"`
- `"demonstrate the integral of x^2 from -1 to 1"`
- `"plot the area under the curve y = x^2"`

## API Usage

### SVG Version
```python
from matvis_simple import MathVisualizationGenerator

generator = MathVisualizationGenerator()
output_path = generator.generate_visualization(
    "plot the function f(x) = x^2",
    output_file="my_quadratic"
)
print(f"SVG saved to: {output_path}")
```

### Matplotlib Version
```python
from matvis import MathVisualizationGenerator

generator = MathVisualizationGenerator()
output_path = generator.generate_visualization(
    "plot the function f(x) = x^2",
    output_file="my_quadratic"
)
print(f"Image saved to: {output_path}")
```

## Testing

Run the test suite to verify functionality:

```bash
python test_simple.py
```

## Output

- **SVG Version**: Generates scalable vector graphics (.svg files) that can be opened in any web browser
- **Matplotlib Version**: Generates high-quality PNG images with proper mathematical notation

## Technical Details

- **SVG Version**: Pure Python implementation with no external dependencies
- **Matplotlib Version**: Uses Matplotlib and NumPy for advanced mathematical plotting
- Supports natural language parsing for mathematical descriptions
- Extensible architecture for adding new mathematical concepts
- Command-line interface with Click

## Project Structure

```
agent-art/
├── matvis_simple.py      # SVG-based implementation (no dependencies)
├── matvis.py            # Matplotlib-based implementation
├── examples_simple.py   # SVG examples
├── examples.py          # Matplotlib examples
├── test_simple.py       # Test suite
├── requirements.txt     # Python dependencies
└── output/             # Generated visualizations
```

## Extending the Application

To add support for new mathematical concepts:

1. Add keyword patterns to `parse_description()` method
2. Create new visualization functions for the concept
3. Update the visualization selection logic in `generate_visualization()`

## Future Enhancements

The codebase is designed to be easily extended with:
- Manim integration for animated videos (planned in matvis.py)
- Interactive visualizations with Plotly
- 3D visualizations
- Web interface for easier access

## Requirements

- **SVG Version**: Python 3.7+ (no additional dependencies)
- **Matplotlib Version**: Python 3.7+, Matplotlib, NumPy, Click, Pillow

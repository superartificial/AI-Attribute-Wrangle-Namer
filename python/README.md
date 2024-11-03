# Houdini Wrangle Namer

An AI-powered tool for automatically naming and documenting AttributeWrangle nodes in SideFX Houdini based on their VEX code.

## Features

- Automatically generates descriptive names for AttributeWrangle nodes based on their VEX code
- Creates detailed documentation in node comments
- Uses OpenAI's GPT-4 for intelligent analysis
- Supports batch processing of multiple nodes
- Progress tracking with UI feedback
- Detailed error reporting

## Installation

1. Clone this repository to your local machine:
```bash
git clone https://github.com/yourusername/houdini_wrangle_namer.git
```

2. Install the required Python package:
```bash
pip install openai>=1.0.0
```

3. Set up your OpenAI API key:
   - Replace the API_KEY variable in the script with your OpenAI API key
   - Or set it as an environment variable

## Usage

1. Copy `wrangle_namer.py` to your Houdini Python scripts directory
2. In Houdini:
   - Select one or more AttributeWrangle nodes
   - Run the script using Python Editor or create a shelf tool
   - The script will automatically:
     - Analyze the VEX code
     - Generate appropriate names
     - Add documentation as comments
     - Display progress and any errors in the UI

## Configuration

The script includes several configuration options at the top:

```python
DEBUG = True                     # Print debug information
ADD_COMMENTS = True             # Add descriptions as node comments
DISPLAY_COMMENTS = True         # Show comments in network view
OPENAI_MODEL = "gpt-4"         # OpenAI model to use
```

## Requirements

- Houdini 19.5 or later
- Python 3.7+
- OpenAI API key
- `openai` Python package version 1.0.0 or later

## License

[MIT License](LICENSE)
# AI Houdini Attribute Wrangle Namer

An AI-powered Houdini shelf tool for automatically naming and documenting AttributeWrangle nodes in SideFX Houdini based on their VEX code.

This version uses OpenAI, with gpt-4o as the default model. It can easily be changed to use a different OpenAI model, and could be adapted to support other vendors (though that would require altering the code to add the appropriate libraries)

## Features

- Automatically generates descriptive names for selected Attribute Wrangle nodes based on their VEX code
- Creates breif documentation in node comments
- Will name multiple attribute wrangles in one click if more than one selected (other nodes are ignored)


## Installation

1) Install the OpenAI library for Houdini's Python:

"path/to/houdini/python.exe" -m pip install --upgrade openai

Note that installing for your global Python won't work. If you don't know the location for the correct python.exe you can find it by running this in the Python shell:

import sys
print(sys.executable)

2) Create a new shelf tool, with the contents of python/wrangle_namer.py copied into the script tab

3) Set up your OpenAI API key:
   - Replace the API_KEY variable in the script with your OpenAI API key
   - Or set it as an environment variable (this requires a code change, and setting up the env variable, and I haven't tested with it: API_KEY = os.getenv('OPENAI_API_KEY', ''))

4) Adding a keyboard shortcut for the shelf tool is also recommended if you plan to use it frequently

## Usage

Select one or more attribute wrange nodes, and run the tool.

## Configuration

The script includes several configuration options at the top:

```python
DEBUG = True                     # Print debug information
ADD_COMMENTS = True             # Add descriptions as node comments
DISPLAY_COMMENTS = True         # Show comments in network view
OPENAI_MODEL = "gpt-4o"         # OpenAI model to use
```

## Requirements

- Houdini 19.5 or later (may work on earlier versions)
- Python 3.7+ (again possibly earlier will work)
- OpenAI API key
- `openai` Python package version 1.0.0 or later

## License

[MIT License](LICENSE)
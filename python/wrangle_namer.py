import hou
import openai
import re
from openai import AsyncOpenAI

# Configuration
DEBUG = True                     # Print debug information
ADD_COMMENTS = True             # Add descriptions as node comments
DISPLAY_COMMENTS = True         # Show comments in network view
OPENAI_MODEL = "gpt-4o"         # OpenAI model to use
API_KEY = "your_openai_key"

# Initialize the OpenAI client
client = AsyncOpenAI(api_key=API_KEY)

def clean_vex_code(code):
    """Remove comments and clean up VEX code for better AI processing."""
    if DEBUG:
        print(f"Original code:\n{code}")
    
    # Remove single-line comments
    code = re.sub(r'//.*$', '', code, flags=re.MULTILINE)
    # Remove multi-line comments
    code = re.sub(r'/\*.*?\*/', '', code, flags=re.DOTALL)
    # Remove empty lines and extra whitespace
    code = '\n'.join(line.strip() for line in code.split('\n') if line.strip())
    
    if DEBUG:
        print(f"Cleaned code:\n{code}")
    return code

async def get_wrangle_analysis(code):
    """Use OpenAI to generate both a name and description for the VEX code."""
    try:
        if DEBUG:
            print("Sending request to OpenAI...")
        response = await client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[
                {"role": "system", "content": """You are a VEX code analyzer. Provide two things:
                1. A brief name (3-4 words using only lowercase letters and underscores)
                2. A breif explanation of what the code does, written in the style of an 
                experienced technical writer. Be succinct by avoiding 
                unnecessary phrases such as "This code snippet" or "This VEX code" (or anything similarly redundant) and basic operations such as 
                variable initialization. This should read is if written by the same team who writes official Houdini documentation. Avoid repetition or 
                stating things that should be obvious to somewith with VEX knowledge. 
                
                Format your response exactly as:
                NAME: your_suggested_name
                DESCRIPTION: Your detailed explanation here."""},
                {"role": "user", "content": f"VEX code:\n{code}"}
            ],
            max_tokens=200,
            temperature=0.3
        )
        
        result = response.choices[0].message.content.strip()
        if DEBUG:
            print(f"Received from OpenAI: {result}")
        
        # Parse the response
        name_match = re.search(r'NAME: (.*?)(?:\n|$)', result)
        desc_match = re.search(r'DESCRIPTION: (.*)', result, re.DOTALL)
        
        name = name_match.group(1).strip() if name_match else "unnamed_wrangle"
        name = name.replace(" ", "_")
        description = desc_match.group(1).strip() if desc_match else "No description available"
        
        return name, description
    except Exception as e:
        if DEBUG:
            print(f"Error in OpenAI request: {str(e)}")
        return f"error_naming_node_{str(e)[:20]}", f"Error occurred: {str(e)}"

async def suggest_wrangle_name():
    """Main function to suggest names for selected attribute wrangles and add descriptions."""
    try:
        # Get selected nodes
        selected_nodes = hou.selectedNodes()
        if DEBUG:
            print(f"Selected nodes: {selected_nodes}")
        
        # Filter for attribute wrangle nodes
        wrangle_nodes = [node for node in selected_nodes if node.type().name() == 'attribwrangle']
        if DEBUG:
            print(f"Found wrangle nodes: {wrangle_nodes}")
        
        if not wrangle_nodes:
            raise hou.Error("Please select at least one Attribute Wrangle node.")
        
        # Process each wrangle node using the progress bar
        with hou.InterruptableOperation(
            "Processing Wrangles - %d nodes" % len(wrangle_nodes), 
            open_interrupt_dialog=True
        ) as progress:
            total_nodes = len(wrangle_nodes)
            
            for index, node in enumerate(wrangle_nodes):
                # Update progress
                progress.updateProgress(float(index) / total_nodes)
                
                if DEBUG:
                    print(f"\nProcessing node: {node.path()}")
                
                # Get the VEX code from the node
                vex_code = node.parm('snippet').eval()
                
                # Clean the code
                cleaned_code = clean_vex_code(vex_code)
                
                if not cleaned_code:
                    if DEBUG:
                        print("No code found in node, skipping...")
                    continue
                
                # Get AI suggestion for both name and description
                suggested_name, description = await get_wrangle_analysis(cleaned_code)
                if DEBUG:
                    print(f"Suggested name: {suggested_name}")
                    print(f"Description: {description}")
                
                # Set the node name
                try:
                    old_name = node.name()
                    node.setName(suggested_name, unique_name=True)
                    if DEBUG:
                        print(f"Successfully renamed node from {old_name} to {node.name()}")
                    
                    # Set the node comment if enabled
                    if ADD_COMMENTS:
                        node.setComment(description)
                        if DISPLAY_COMMENTS:
                            node.setGenericFlag(hou.nodeFlag.DisplayComment, True)
                        if DEBUG:
                            print("Successfully added and displayed comment")
                    
                except hou.OperationFailed as e:
                    if DEBUG:
                        print(f"Failed to rename node: {str(e)}")
            
            # Update progress to completion
            progress.updateProgress(1.0)
            
    except Exception as e:
        if DEBUG:
            print(f"Error in suggest_wrangle_name: {str(e)}")
        raise

def run_async_script():
    """Helper function to run async code in sync context"""
    try:
        import asyncio
        asyncio.run(suggest_wrangle_name())
    except RuntimeError as e:
        # Handle case where event loop is already running
        loop = asyncio.get_event_loop()
        loop.run_until_complete(suggest_wrangle_name())

if DEBUG:
    print("Starting script...")
run_async_script()
if DEBUG:
    print("Script finished!")
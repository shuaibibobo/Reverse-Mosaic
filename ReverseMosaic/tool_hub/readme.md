# Guide for Creating a Tool in Reverse Mosaic
Creating a tool in Reverse Mosaic involves defining a function that performs a specific analysis task on binary files. This guide will walk you through the process of creating a tool, including where to store it to be automatically picked up by Reverse Mosaic, adding a requirements.txt file for dependencies, and understanding how the tools work within the toolkit.

## Tool Creation
### Define a Function
Start by defining a Python function that performs the desired analysis on binary files. This function should take the binary file path as input and return the analysis result.

Here's an example of a simple tool function that retrieves the file type of a binary file:

```python
import magic

def get_file_type(file_path):
    """
    Retrieves the file type of the given binary file.

    Args:
        file_path (str): The path to the binary file.

    Returns:
        str: The file type.
    """
    return magic.from_file(file_path, mime=True)
```

### Create a Tool Class
Next, create a class that encapsulates the tool function. This class should inherit from ```BaseToolClass``` and implement the ```return_tools``` method, which returns a list of ```FunctionTool``` instances.

```python
from llama_index.core.tools import FunctionTool
from tool_hub.base_tool import BaseToolClass

class FileTypeTool(BaseToolClass):
    """A tool for retrieving file type from a binary."""

    @staticmethod
    def get_file_type(file_path):
        """
        Retrieves the file type of the given binary file.

        Args:
            file_path (str): The path to the binary file.

        Returns:
            str: The file type.
        """
        return magic.from_file(file_path, mime=True)

    @staticmethod
    def return_tools():
        """Returns a list of FunctionTool instances for file type retrieval."""
        list_of_functions = [
            FileTypeTool.get_file_type,
        ]

        tools = []
        for fun in list_of_functions:
            tool = FunctionTool.from_defaults(fun,)
            tools.append(tool)

        return tools
```

### Store the Tool
Store the tool in the appropriate directory structure to be automatically picked up by Reverse Mosaic. Place the tool file inside the ```tool_hub/tools``` directory.

```
ReverseMosaic/
├── tool_hub/
│   ├── tools/
│   │   └── file_type_tool.py   <-- Your tool file
```

### Add get_class Function
Each tool file should include a ```get_class``` function that returns an instance of the tool class.

```python
def get_class():
    return FileTypeTool()
```

## Dependencies
### Requirements.txt
Create a requirements.txt file in the same directory as your tool. This file should list all the dependencies required for your tool.

```
ReverseMosaic/
├── tool_hub/
│   ├── tools/
│   │   ├── file_type_tool.py
│   │   └── requirements.txt   <-- Your requirements file
```

Example requirements.txt:

```
python-magic
```

## How Tools Work
### Tool Execution
When Reverse Mosaic executes, it automatically scans the ```tool_hub/tools``` directory for Python files containing tool classes inheriting from BaseToolClass. It then loads these classes and retrieves the tools using the return_tools method.

### Tool Structure
Each tool class should define one or more static methods that perform specific analysis tasks. These methods take the binary file path as input and return the analysis result. The return_tools method creates FunctionTool instances for each tool method, making them accessible within Reverse Mosaic.

### Integration with Reverse Mosaic
Once the tools are loaded, Reverse Mosaic can utilize them to perform analysis tasks based on deployment directives or user requests. Tools are executed within the multi-agent architecture of Reverse Mosaic, allowing for efficient and scalable analysis of binary files.

# Conclusion
By following this guide, you can create custom tools for Reverse Mosaic to extend its capabilities and perform specialized analysis tasks on binary files. Remember to structure your tools properly, add dependencies to the requirements.txt file, and store them in the designated directory for seamless integration with Reverse Mosaic.






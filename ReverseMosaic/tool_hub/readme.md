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
Next, create a class that encapsulates the tool function. This class should inherit from ```BaseToolClass``` and implement the ```get_tool_functions``` method, which returns a list of all function (tools) that you want the Reverse Mosaic agent to use. Ensure to use docstrings and type-hinting as these allow the agent to fully understand the function.

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
    def get_tool_functions():
        """Returns a list of FunctionTool instances for file type retrieval."""
        list_of_functions = [
            FileTypeTool.get_file_type,
        ]

        return list_of_functions
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

<p align="center"> <img margin-right: auto width=25% src="../../small-logo.png"> </p>




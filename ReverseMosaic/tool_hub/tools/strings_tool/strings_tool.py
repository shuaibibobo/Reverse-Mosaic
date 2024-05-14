from llama_index.core.tools import FunctionTool
import subprocess
import sys
import tempfile
import re
from tool_hub.base_tool import BaseToolClass

class StringsTool(BaseToolClass):
    """A tool for retrieving strings from a binary."""

    @staticmethod
    def get_strings(binary: str) -> str:
        """Retrieves a list of strings from a binary or file.

        Args:
            binary (str): The path to the binary.

        Returns:
            str: A list of all strings in the binary.
        """
        words = []
        with open(binary, 'rb') as file:
            binary_data = file.read()
            # Convert binary data to string
            text = binary_data.decode('utf-8', errors='ignore')
            
            # Use regular expression to find words
            word_regex = re.compile(r'\b[a-zA-Z]+\b')
            words = word_regex.findall(text)
            
        return words



    def return_tools(self) -> list:
        """Returns a list of FunctionTool instances for Ghidra-related functions.

        Returns:
            list: A list of FunctionTool instances.
        """
        list_of_functions = [
            StringsTool.get_strings,
        ]

        tools = []
        for fun in list_of_functions:
            tool = FunctionTool.from_defaults(fun,)
            tools.append(tool)

        return tools
    
def get_class():
    return StringsTool()

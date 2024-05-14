from llama_index.core.tools import FunctionTool
import re
import magic
from tool_hub.base_tool import BaseToolClass

class FileTypeTool(BaseToolClass):
    """A tool for retrieving file type from a binary."""

    @staticmethod
    def get_file_type(file: str) -> str:
        """
        Retrieves the file type of the given binary/ file.

        Parameters:
        file (str): The path to the binary.

        Returns:
        str: The file type.
        """
        return magic.from_file(file, mime=True)


    def return_tools(self) -> list:
        """Returns a list of FunctionTool instances for Ghidra-related functions.

        Returns:
            list: A list of FunctionTool instances.
        """
        list_of_functions = [
            FileTypeTool.get_file_type,
        ]

        tools = []
        for fun in list_of_functions:
            tool = FunctionTool.from_defaults(fun,)
            tools.append(tool)

        return tools
    
def get_class():
    return FileTypeTool()

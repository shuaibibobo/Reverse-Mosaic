try:
    from ReverseMosaic.tool_hub.base_tool import BaseToolClass
except:
    from tool_hub.base_tool import BaseToolClass
from llama_index.core.tools import FunctionTool
import subprocess
import sys
import tempfile


class FlawFinderTool(BaseToolClass):
    """A tool for interacting with FlawFinder."""

    @staticmethod
    def find_flaws_and_vulnerabilities(c_code: str) -> str:
        """Retrieves information on weaknesses, issues, flaws, and vulnerabilities from provided decompiled C code.

        Args:
            c_code (str): C decompilation

        Returns:
            str: A string containing information about identified issues.
        """

        with tempfile.NamedTemporaryFile(mode='w', delete=False) as temp_file:
            # Write the string to the temporary file
            temp_file.write(c_code)
            # Get the filename of the temporary file
            temp_file_name = temp_file.name
            python_executable_path = sys.executable
            result = subprocess.run([python_executable_path, '-m', 'flawfinder',temp_file_name], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            return result

    def get_tool_functions(self) -> list:
        """Returns a list of tools for Ghidra-related functions.

        Returns:
            list: A list of functions.
        """
        list_of_functions = [
            FlawFinderTool.find_flaws_and_vulnerabilities,
        ]

        return list_of_functions
    
def get_class():
    return FlawFinderTool()

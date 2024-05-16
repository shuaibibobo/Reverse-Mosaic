try:
    from ReverseMosaic.tool_hub.base_tool import BaseToolClass
except:
    from tool_hub.base_tool import BaseToolClass
try:
    from ReverseMosaic.tool_hub.tools.ghidra_tool.GhidraBridge.ghidra_bridge import GhidraBridge
except:
    from tool_hub.tools.ghidra_tool.GhidraBridge.ghidra_bridge import GhidraBridge
from llama_index.core.tools import FunctionTool


class GhidraTool(BaseToolClass):
    """A tool for interacting with Ghidra."""

    @staticmethod
    def get_all_function_names_and_addresses(binary: str) -> str:
        """Retrieves all function names and their respective addresses in the binary.

        Args:
            binary (str): The path to the binary.

        Returns:
            str: A string containing all function names and addresses.
        """
        bridge = GhidraBridge()

        script = bridge.generate_get_function_names_and_address()
        out = bridge.run_string_script_on_binary(script, binary)

        preamble, out = str(out).split("script.py (HeadlessAnalyzer)")
        out, amble = out.split("INFO  ANALYZING changes made by post scripts")

        out = out.replace(r"\n", " ")
        out = out.replace(r"\r", " ")
        out = out.strip()

        return out

    @staticmethod
    def get_cross_references_to_function_name(function_name: str, binary: str) -> str:
        """Retrieves a list of cross references to a given function name.

        Args:
            function_name (str): The name of the function.
            binary (str): The path to the binary.

        Returns:
            str: A string containing cross references to the function.
        """
        bridge = GhidraBridge()

        script = bridge.generate_get_cross_references_to_function_name(function_name)
        out = bridge.run_string_script_on_binary(script, binary)

        preamble, out = str(out).split("script.py (HeadlessAnalyzer)")
        out, amble = out.split("INFO  ANALYZING changes made by post scripts")

        out = out.replace(r"\n", " ")
        out = out.replace(r"\r", " ")
        out = out.strip()

        return out

    @staticmethod
    def get_decom_for_function(function_name: str, binary: str) -> str:
        """Decompiles a function of a binary and returns the decompiled C code.

        Args:
            function_name (str): The name of the function.
            binary (str): The path to the binary.

        Returns:
            str: The decompiled C code of the function.
        """
        bridge = GhidraBridge()

        script = bridge.generate_decom_for_function(function_name)
        out = bridge.run_string_script_on_binary(script, binary)

        preamble, out = str(out).split("script.py (HeadlessAnalyzer)")
        out, amble = out.split("INFO  ANALYZING changes made by post scripts")

        out = out.replace(r"\n", " ")
        out = out.replace(r"\r", " ")
        out = out.strip()

        return out

    @staticmethod
    def get_function_address_by_name(function_name: str, binary: str) -> str:
        """Retrieves the address of a function in the binary.

        Args:
            function_name (str): The name of the function.
            binary (str): The path to the binary.

        Returns:
            str: The address of the function.
        """
        bridge = GhidraBridge()

        script = bridge.generate_get_function_address_by_name(function_name)
        out = bridge.run_string_script_on_binary(script, binary)

        preamble, out = str(out).split("script.py (HeadlessAnalyzer)")
        out, amble = out.split("INFO  ANALYZING changes made by post scripts")

        out = out.replace(r"\n", " ")
        out = out.replace(r"\r", " ")
        out = out.strip()

        return out

    @staticmethod
    def get_function_name_by_address(function_address: str, binary: str) -> str:
        """Retrieves the name of a function in the binary.

        Args:
            function_address (str): The address of the function.
            binary (str): The path to the binary.

        Returns:
            str: The name of the function.
        """
        bridge = GhidraBridge()

        script = bridge.generate_get_a_function_name_by_address(function_address)
        out = bridge.run_string_script_on_binary(script, binary)

        preamble, out = str(out).split("script.py (HeadlessAnalyzer)")
        out, amble = out.split("INFO  ANALYZING changes made by post scripts")

        out = out.replace(r"\n", " ")
        out = out.replace(r"\r", " ")
        out = out.strip()

        return out

    def get_tool_functions(self) -> list:
        """Returns a list of functions for Ghidra-related functions.

        Returns:
            list: A list of functions.
        """
        list_of_functions = [
            GhidraTool.get_all_function_names_and_addresses,
            GhidraTool.get_cross_references_to_function_name,
            GhidraTool.get_decom_for_function,
            GhidraTool.get_function_address_by_name,
            GhidraTool.get_function_name_by_address
        ]
        return list_of_functions

def get_class():
    return GhidraTool()

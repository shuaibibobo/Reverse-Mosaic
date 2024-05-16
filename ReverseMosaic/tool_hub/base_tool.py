from llama_index.core.tools import FunctionTool

class BaseToolClass:

    def get_tool_functions()-> list:
        """Returns a list of functions that can be run as tools by the multi agent"""
        raise Exception("Not overriden exception")
        return []

    def return_tools(self) -> list:
        """Returns a list of FunctionTool instances for Ghidra-related functions.

        Returns:
            list: A list of FunctionTool instances.
        """

        list_of_functions = self.get_tool_functions()
        tools = []
        for fun in list_of_functions:
            tool = FunctionTool.from_defaults(fun,)
            tools.append(tool)

        return tools
    

def get_class():
    return BaseToolClass()

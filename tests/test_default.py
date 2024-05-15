import os
import pytest
from unittest.mock import MagicMock, patch
from tempfile import NamedTemporaryFile
from ReverseMosaic import RMSecAgent 
from ReverseMosaic.agent_helper import AgentHelper
from ReverseMosaic.tool_hub.tools.flaw_finder_tool.flaw_finder_tool import FlawFinderTool
from ReverseMosaic.tool_hub.tools.ghidra_tool.ghidra_tool import GhidraTool
from ReverseMosaic.tool_hub.tools.strings_tool.strings_tool import StringsTool

# Test data generation
PDF_CONTENT = b"This is a sample PDF content."
BINARY_CONTENT = b"\x48\x65\x6c\x6c\x6f\x20\x77\x6f\x72\x6c\x64\x21"

# Mocking the console
console_mock = MagicMock()

# Test AgentHelper class
class TestAgentHelper:
    C_CODE = """
    #include <stdio.h>

    int main() {
        printf("Hello, world!");
        return 0;
    }
    """
    def test_execute_steps(self):
        helper = AgentHelper()
        agent = MagicMock()
        task = MagicMock()
        with patch("builtins.print") as mock_print:
            response = helper.execute_steps(agent, task, console_mock)
            assert response is not None
            mock_print.assert_called()
    
    def test_load_model(self):
        helper = AgentHelper()
        model, tokenizer = helper.load_model()
        assert model is not None
        assert tokenizer is not None
    
    def test_get_llm(self):
        helper = AgentHelper()
        llm = helper.get_llm()
        assert llm is not None
    
    def test_generate_tool(self):
        helper = AgentHelper()
        with NamedTemporaryFile(delete=False) as temp_pdf:
            temp_pdf.write(PDF_CONTENT)
            pdf_file_path = temp_pdf.name
        
        tool = helper.generate_tool("test_tool", pdf_file_path, "working", "This is a sample PDF description.")
        assert tool is not None
        
        # Clean up
        os.remove(pdf_file_path)

# Test FlawFinderTool class
class TestFlawFinderTool:
    
    def test_return_tools(self):
        tool = FlawFinderTool()
        tools = tool.return_tools()
        assert isinstance(tools, list)

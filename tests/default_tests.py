import os
import pytest
from unittest.mock import MagicMock, patch
from tempfile import NamedTemporaryFile
from ReverseMosaic import RMSecAgent, AgentHelper
from ReverseMosaic.tool_hub.tools import FlawFinderTool, GhidraTool, StringsTool

# Test data generation
PDF_CONTENT = b"This is a sample PDF content."
BINARY_CONTENT = b"\x48\x65\x6c\x6c\x6f\x20\x77\x6f\x72\x6c\x64\x21"

# Mocking the console
console_mock = MagicMock()

# Test RMSecAgent class
class TestRMSecAgent:
    
    def test_generate_tool_brief_pdf_file_not_found(self):
        agent = RMSecAgent()
        with pytest.raises(FileNotFoundError):
            agent.generate_tool_brief("invalid_path.pdf")
    
    def test_generate_tool_brief(self):
        # Write PDF content to temporary file
        with NamedTemporaryFile(delete=False) as temp_pdf:
            temp_pdf.write(PDF_CONTENT)
            pdf_file_path = temp_pdf.name
        
        agent = RMSecAgent()
        agent.generate_tool_brief(pdf_file_path, should_get_pdf_text=False, should_add_name=False)
        
        # Assert generated JSON file exists
        assert os.path.exists("working/briefs/sample.json")
        
        # Clean up
        os.remove("working/briefs/sample.json")
        os.remove(pdf_file_path)
    
    def test_scan_working_dir(self):
        agent = RMSecAgent()
        briefs = agent.scan_working_dir()
        assert isinstance(briefs, list)
    
    def test_generate_briefs_from_directory(self):
        agent = RMSecAgent()
        agent.generate_briefs_from_directory("test_data")
        assert os.path.exists("working/briefs/sample.json")
        os.remove("working/briefs/sample.json")
    
    def test_query_agent(self):
        agent = RMSecAgent()
        response = agent.query_agent("deploy some tools")
        assert isinstance(response, str)

# Test AgentHelper class
class TestAgentHelper:
    
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
    
    def test_find_flaws_and_vulnerabilities(self):
        result = FlawFinderTool.find_flaws_and_vulnerabilities("sample C code")
        assert result is not None
    
    def test_return_tools(self):
        tool = FlawFinderTool()
        tools = tool.return_tools()
        assert isinstance(tools, list)

# Test GhidraTool class
class TestGhidraTool:
    
    def test_get_all_function_names_and_addresses(self):
        result = GhidraTool.get_all_function_names_and_addresses("sample binary")
        assert result is not None
    
    def test_get_cross_references_to_function_name(self):
        result = GhidraTool.get_cross_references_to_function_name("sample_function", "sample binary")
        assert result is not None
    
    def test_get_decom_for_function(self):
        result = GhidraTool.get_decom_for_function("sample_function", "sample binary")
        assert result is not None
    
    def test_get_function_address_by_name(self):
        result = GhidraTool.get_function_address_by_name("sample_function", "sample binary")
        assert result is not None
    
    def test_get_function_name_by_address(self):
        result = GhidraTool.get_function_name_by_address("sample_address", "sample binary")
        assert result is not None
    
    def test_return_tools(self):
        tool = GhidraTool()
        tools = tool.return_tools()
        assert isinstance(tools, list)

# Test StringsTool class
class TestStringsTool:
    
    def test_get_strings(self):
        result = StringsTool.get_strings("sample binary")
        assert result is not None
    
    def test_return_tools(self):
        tool = StringsTool()
        tools = tool.return_tools()
        assert isinstance(tools, list)

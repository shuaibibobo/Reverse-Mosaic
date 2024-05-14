import os
import json
import importlib.util
import argparse
from rich.console import Console
from misc_helper import get_text_from_pdf
from agent_helper import AgentHelper
from llama_index.core.agent import ReActAgent
import gc 
import warnings

class RMSecAgent:
    """
    A class to manage the operations of an RMSecAgent.

    Attributes:
        working_dir (str): The directory name for storing working data.
        agent_help (AgentHelper): An instance of AgentHelper to assist with agent operations.
    """

    working_dir = "working"
    agent_help = None

    def __init__(self):
        """
        Initializes RMSecAgent with an instance of AgentHelper.
        """
        self.agent_help = AgentHelper()

    def generate_tool_brief(self, pdf_file_path, should_get_pdf_text=True, should_add_name=False):
        """
        Generates a tool brief from a PDF file.

        Args:
            pdf_file_path (str): The path to the PDF file.
            should_get_pdf_text (bool, optional): Whether to extract text from the PDF. Defaults to True.
            should_add_name (bool, optional): Whether to prompt for a tool name. Defaults to False.
        """
        # Check if file exists and is a PDF
        if not os.path.exists(pdf_file_path) or not pdf_file_path.lower().endswith('.pdf'):
            print("Invalid PDF file.")
            return

        # Extract file name
        file_name = os.path.basename(pdf_file_path).replace(".pdf", "")
        
        # Get the directory of the script
        script_dir = os.path.dirname(os.path.realpath(__file__))
        
        # Create a working directory
        working_dir = os.path.join(script_dir, self.working_dir, file_name)
        os.makedirs(working_dir, exist_ok=True)
        
        if should_get_pdf_text:
            description = get_text_from_pdf(pdf_file_path)
        else:
            description = input(f"What is the description for {file_name}? ")

        if should_add_name:
            file_name = input(f"What is the name for {file_name}? ")
        
        # Create JSON data
        pdf_data = {
            "file_path": pdf_file_path,
            "file_name": file_name,
            "working_dir": working_dir,
            "description": description
        }
        
        # Write JSON to a file in the "briefs" subfolder
        briefs_dir = os.path.join(script_dir, self.working_dir, "briefs")
        os.makedirs(briefs_dir, exist_ok=True)
        json_file_path = os.path.join(briefs_dir, file_name + ".json")
        with open(json_file_path, "w") as json_file:
            json.dump(pdf_data, json_file, indent=4)
        
        print("Brief generated for PDF file:", file_name)
        print("JSON file created at:", json_file_path)

    def scan_working_dir(self):
        """
        Scans the working directory for tool briefs.

        Returns:
            list: A list of tool brief dictionaries.
        """
        # Get the directory of the script
        script_dir = os.path.dirname(os.path.realpath(__file__))
        
        # Define the working directory
        working_dir = os.path.join(script_dir, self.working_dir, "briefs")
        
        # Check if working directory exists
        if not os.path.exists(working_dir):
            print("Working directory doesn't exist.")
            return []
        
        # Initialize list to store data
        pdf_data_list = []
        
        # Scan working directory for JSON files
        for root, dirs, files in os.walk(working_dir):
            for file in files:
                if file.endswith(".json"):
                    json_file_path = os.path.join(root, file)
                    with open(json_file_path, "r") as json_file:
                        pdf_data = json.load(json_file)
                        # Check if working directory and PDF file still exist
                        if not os.path.exists(pdf_data["working_dir"]) or not os.path.exists(pdf_data["file_path"]):
                            print(f"Warning: PDF or working directory missing for {pdf_data['file_name']}. Ignoring.")
                            continue
                        pdf_data_list.append(pdf_data)
        
        return pdf_data_list

    def generate_briefs_from_directory(self, directory):
        """
        Generates tool briefs from PDF files in a directory.

        Args:
            directory (str): The directory path.
        """
        # Check if the directory exists
        if not os.path.exists(directory) or not os.path.isdir(directory):
            print("Invalid directory.")
            return
        
        # Get the list of PDF files in the directory
        pdf_files = [file for file in os.listdir(directory) if file.lower().endswith('.pdf')]
        
        if not pdf_files:
            print("No PDF files found in the directory.")
            return
        
        for pdf_file in pdf_files:
            pdf_file_path = os.path.join(directory, pdf_file)
            self.generate_tool_brief(pdf_file_path)

    def query_agent(self, deployment_directive):
        """
        Queries the agent based on a deployment directive.

        Args:
            deployment_directive (str): The deployment directive.

        Returns:
            str: The response from the agent.
        """
        console = Console()

        tool_briefs = self.scan_working_dir()
        tools = []
        console.clear()
        with console.status("[bold green]Working on inheriting tools...") as status:
            
            folder_path = r"tool_hub\tools"
            for root, dirs, files in os.walk(os.path.join(__file__, "..", folder_path)):
                for dir in dirs:
                    subfolder_path = os.path.join(root, dir)
                    if "tool" in dir.lower():
                        for file_name in os.listdir(subfolder_path):
                            if file_name.endswith(".py") and not file_name.startswith("__"):
                                module_name = file_name[:-3]  # Remove the .py extension
                                module_path = os.path.join(subfolder_path, file_name)

                                spec = importlib.util.spec_from_file_location(module_name, module_path)
                                mod = importlib.util.module_from_spec(spec)

                                spec.loader.exec_module(mod)

                                returned_tools = mod.get_class().return_tools()
                                tools = tools + returned_tools
                                    
                                console.log(f"Inherited {len(returned_tools)} tool(s) from {module_name} in tool hub")

            for brief in tool_briefs:
                tool_name = brief["file_name"].replace(".pdf","")
                tool_path = brief["file_path"]
                tool_working_dir = brief["working_dir"]
                tool_description = brief["description"]

                tool = self.agent_help.generate_tool(tool_name, tool_path, tool_working_dir, tool_description)
                tools.append(tool)
                console.log(f"Inherited {tool_name} tool from PDF briefs")
                gc.collect()

        console.clear()
        agent = ReActAgent.from_tools(
            tools,
            llm=self.agent_help.get_llm(),
            verbose=True,
            # context=context
        )

        console.log("Starting task!")
        
        task = agent.create_task(
            deployment_directive,
        )

        response = self.agent_help.execute_steps(agent, task, console)

        return response

def pass_deployment_directive(deployment_directive):
    """
    Entrypoint for sending a deployment directive/ query directly
    """
    sec_agent = RMSecAgent()
    print(sec_agent.query_agent(deployment_directive))

def run():
    """
    Parses command-line arguments and runs the RMSecAgent accordingly.
    """
    parser = argparse.ArgumentParser(description="PDF Tools Builder")

    # Define mutually exclusive group for build_pdf_tools and deployment_directive
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--pdf_tool_data_path", help="Specify the path to build PDF tools")
    group.add_argument("--deployment_directive", help="Specify the deployment directive to build PDF tools")
    
    args = parser.parse_args()

    sec_agent = RMSecAgent()

    if args.pdf_tool_data_path:
        sec_agent.generate_briefs_from_directory(args.pdf_tool_data_path)
    elif args.deployment_directive:
        print(sec_agent.query_agent(args.deployment_directive))
    else:
        raise Exception("No args provided")

if __name__ == "__main__":

    try:
        with warnings.catch_warnings(action="ignore"):
            run()
    except:
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore")
            run()

import os
import subprocess
import platform
import argparse
import sys
from typing import Optional
import shutil

def is_venv_active() -> bool:
    """Check if a virtual environment is active."""
    return hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)

def create_venv(venv_path: str, python_executable: str) -> None:
    """Create a virtual environment."""
    subprocess.run([python_executable, "-m", "venv", venv_path])

def install_requirements(python_executable: str, requirements_file: str) -> None:
    """Install requirements from a file."""
    subprocess.run([python_executable, "-m", "pip", "install", "-r", requirements_file])

def search_and_install(tool_hub_path: str, python_executable: str) -> None:
    """Search for subdirectories in tool_hub and install their requirements."""

    for root, dirs, files in os.walk(tool_hub_path):
        for directory in dirs:

            requirements_file = os.path.join(root, directory, "requirements.txt")
            if os.path.isfile(requirements_file):
                print(f"Tool {directory} requirements")
                install_requirements(python_executable, requirements_file)

def copy_folder(source, destination):
    try:
        shutil.copytree(source, destination)
        print(f"Folder copied successfully to {destination}!")
    except shutil.Error as e:
        print(f"Error: {e}")
    except OSError as e:
        print(f"Error: {e}")

def main() -> None:
    """Main function to handle tool installation."""
    parser = argparse.ArgumentParser(description="Tool installation with virtual environment")
    parser.add_argument("python_path", help="Path to python executable")
    args = parser.parse_args()

    python_executable: str = args.python_path

    # Install main requirements if available
    requirements_txt: str = os.path.join(os.path.dirname(os.path.abspath(__file__)), "requirements.txt")
    if os.path.isfile(requirements_txt):
        install_requirements(python_executable, requirements_txt)

    # Search for subdirectories in tool_hub and install their requirements
    tool_hub_path: str = os.path.join(os.path.dirname(os.path.abspath(__file__)),"ReverseMosaic", "tool_hub")
    search_and_install(tool_hub_path, python_executable)

    # Install the package at the root in the venv
    setup_py_path: str = subprocess.run([python_executable, "-m", "pip", "install", "."])

    # Copy Tools
    print("Copying tools folder...")
    home_dir = os.path.expanduser("~")
    source_folder = os.path.join("ReverseMosaic","tool_hub","tools")
    destination_folder = os.path.join(home_dir, ".ReverseMosaic","tool_hub","tools")

    copy_folder(source_folder, destination_folder)


if __name__ == "__main__":
    main()

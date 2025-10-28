import argparse
import subprocess
import sys
import os
import venv
from pathlib import Path

def create_venv(venv_name):
    """Create a virtual environment with the given name"""
    try:
        print(f"Creating virtual environment: {venv_name}")
        venv.create(venv_name, with_pip=True)
        print(f"Virtual environment created successfully at: {venv_name}")
    except Exception as e:
        print(f"Error creating virtual environment: {e}")
        sys.exit(1)

def get_venv_python(venv_name):
    """Get the Python executable path from the virtual environment"""
    if os.name == 'nt':  # Windows
        return os.path.join(venv_name, 'Scripts', 'python.exe')
    return os.path.join(venv_name, 'bin', 'python')

def get_available_requirement_files():
    """Get all requirement files in current directory"""
    return [f.name for f in Path().glob("*Requirements.txt")]

def install_requirements(req_file, venv_python):
    """Install requirements from specified file"""
    try:
        print(f"Installing requirements from {req_file}...")
        subprocess.check_call([venv_python, "-m", "pip", "install", "-r", req_file])
        print(f"Successfully installed requirements from {req_file}")
    except subprocess.CalledProcessError as e:
        print(f"Error installing requirements from {req_file}: {e}")
        sys.exit(1)

def main():
    # Get available requirement files
    req_files = get_available_requirement_files()
    
    # Setup argument parser
    parser = argparse.ArgumentParser(description='Install Python packages from different requirement files')
    parser.add_argument('--type', choices=req_files, help='Type of requirements to install')
    parser.add_argument('--all', action='store_true', help='Install all requirements')
    parser.add_argument('--venv', default='temp_setup', help='Name of the virtual environment (default: temp_setup)')
    
    args = parser.parse_args()
    
    if not args.type and not args.all:
        print("Please specify either --type or --all")
        print("\nAvailable requirement types:")
        for rf in req_files:
            print(f"  - {rf}")
        sys.exit(1)
    
    # Create virtual environment
    create_venv(args.venv)
    venv_python = get_venv_python(args.venv)
    
    if args.all:
        for req_file in req_files:
            install_requirements(req_file, venv_python)
    else:
        install_requirements(args.type, venv_python)
    
    print(f"\nSetup complete! To activate the virtual environment:")
    if os.name == 'nt':  # Windows
        print(f"    {args.venv}\\Scripts\\activate")
    else:  # Unix/Linux
        print(f"    source {args.venv}/bin/activate")

if __name__ == "__main__":
    main()
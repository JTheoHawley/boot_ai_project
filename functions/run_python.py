import os
import subprocess
import sys
from google.genai import types



def run_python_file(working_directory, file_path, args=None):
    work_path = os.path.abspath(os.path.join(working_directory, file_path))
    command = [sys.executable, work_path]
    if args:
        command += args
    if not work_path.startswith(os.path.abspath(working_directory)):
        return(f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory')
    if not os.path.isfile(work_path):
        return(f'Error: File "{file_path}" not found.')
    if not file_path.endswith(".py"):
        return(f'Error: "{file_path}" is not a Python file.')
    try:  
        result = subprocess.run(command, cwd=os.path.abspath(working_directory), timeout=30, capture_output=True, text=True,)

        if result.stdout == "" and result.stderr == "":
            return "No output produced."
        if result.returncode != 0:
            return(f'STDOUT: {result.stdout}\nSTDERR: {result.stderr}\nProcess exited with code {result.returncode}')
        else:
            return(f'STDOUT: {result.stdout}\nSTDERR: {result.stderr}')
    except Exception as e:
        return f"Error: executing Python file: {e}"
    
schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a Python file within the working directory and returns the output from the interpreter.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the Python file to execute, relative to the working directory.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(
                    type=types.Type.STRING,
                    description="Optional arguments to pass to the Python file.",
                ),
                description="Optional arguments to pass to the Python file.",
            ),
        },
        required=["file_path"],
    ),
)
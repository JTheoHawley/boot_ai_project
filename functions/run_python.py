import os
import subprocess
import sys


def run_python_file(working_directory, file_path):
    work_path = os.path.abspath(os.path.join(working_directory, file_path))
    if not work_path.startswith(os.path.abspath(working_directory)):
        return(f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory')
    if not os.path.isfile(work_path):
        return(f'Error: File "{file_path}" not found.')
    if not file_path.endswith(".py"):
        return(f'Error: "{file_path}" is not a Python file.')
    try:  
        result = subprocess.run([sys.executable, work_path], cwd=os.path.abspath(working_directory), timeout=30, capture_output=True, text=True)
        if result.stdout == "" and result.stderr == "":
            return "No output produced."
        if result.returncode != 0:
            return(f'STDOUT: {result.stdout}\nSTDERR: {result.stderr}\nProcess exited with code {result.returncode}')
        else:
            return(f'STDOUT: {result.stdout}\nSTDERR: {result.stderr}')
    except Exception as e:
        return f"Error: executing Python file: {e}"
import os
from google.genai import types


def get_files_info(working_directory, directory=None):
    work_path = os.path.abspath(os.path.join(working_directory, directory))
    if not work_path.startswith(os.path.abspath(working_directory)):
        return(f'Error: Cannot list "{directory}" as it is outside the permitted working directory')
    if not os.path.isdir(work_path):
        return(f'Error: "{directory}" is not a directory')
    else:
        names = os.listdir(work_path)
        s_list = []
        for name in names:
            path = os.path.join(work_path, name)
            size = os.path.getsize(path)
            is_dir = os.path.isdir(path)
            s_list.append(f"- {name}: file_size={size} bytes, is_dir={is_dir}")
        return("\n".join(s_list))
    

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)
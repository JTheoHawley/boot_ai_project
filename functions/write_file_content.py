import os
from google.genai import types


def write_file(working_directory, file_path, content):
    work_path = os.path.abspath(os.path.join(working_directory, file_path))
    if not work_path.startswith(os.path.abspath(working_directory)):
        return(f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory')
    try:
        os.makedirs(os.path.dirname(work_path), exist_ok=True)
        with open(work_path, "w") as f:
            f.write(content)
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f"Error: {e}"

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes the specified content to the specified file.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file to be written too.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to be written to the specified file."
            ),
        },
    ),
)

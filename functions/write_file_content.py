import os


def write_file(working_directory, file_path, content):
    work_path = os.path.join(working_directory, file_path)
    if not os.path.abspath(work_path).startswith(os.path.abspath(working_directory)):
        return(f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory')
    try:
        os.makedirs(os.path.dirname(work_path), exist_ok=True)
        with open(work_path, "w") as f:
            f.write(content)
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f"Error: {e}"


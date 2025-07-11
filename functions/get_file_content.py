import os



def get_file_content(working_directory, file_path):
    work_path = os.path.abspath(os.path.join(working_directory, file_path))
    if not work_path.startswith(os.path.abspath(working_directory)):
        return(f'Error: Cannot read "{file_path}" as it is outside the permitted working directory')
    if not os.path.isfile(work_path):
        return(f'Error: File not found or is not a regular file: "{file_path}"')
    MAX_CHARS = 10000

    try:
        with open(work_path, "r") as f:
            file_content_string = f.read(MAX_CHARS)
            if f.read(1) == (""):
                return (file_content_string)
            else:
                return (file_content_string + f'[...File "{file_path}" truncated at 10000 characters]')
    except Exception as e:
        return f"Error: {e}"
            
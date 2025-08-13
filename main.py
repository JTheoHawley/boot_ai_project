import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import schema_get_files_info, get_files_info
from functions.get_file_content import schema_get_file_content, get_file_content
from functions.run_python import schema_run_python_file, run_python_file
from functions.write_file_content import schema_write_file, write_file

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

user_prompt = sys.argv[1]
messages = [types.Content(role="user", parts=[types.Part(text=user_prompt)]), ]

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file,
    ]
)

function_map = {"get_files_info": get_files_info,
                "get_file_content": get_file_content,
                "run_python_file":run_python_file,
                "write_file": write_file,}

config=types.GenerateContentConfig(
    tools=[available_functions], system_instruction=system_prompt
)

def call_function(function_call_part, verbose=False):
    function_name = function_call_part.name
    function_args = function_call_part.args
    if verbose == True:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_call_part.name}")
    if function_name in function_map:
        function_args["working_directory"] = "./calculator"
        actual_function = function_map[function_name]
        function_result = actual_function(**function_args)
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"result": function_result},
                )
            ],
        )
    else:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
            )
        ],
    )



if len(sys.argv) == 1:
    print("No prompt provided")
    sys.exit(1)
if "--verbose" in sys.argv:
    response = client.models.generate_content(model="gemini-2.0-flash-001", contents=messages, config=config)
    prompt_tokens = response.usage_metadata.prompt_token_count
    response_tokens = response.usage_metadata.candidates_token_count

    if response.function_calls:
        for function_call_part in response.function_calls:
            function_call_result = call_function(function_call_part, verbose=True)
            if (
                not function_call_result.parts
                or not function_call_result.parts[0].function_response
            ):
                raise Exception("empty function call result")            
            print(f"-> {function_call_result.parts[0].function_response.response}")
        print(f"User prompt: {user_prompt}")    
        print(f"Prompt tokens: {prompt_tokens}")
        print(f"Response tokens: {response_tokens}")
    else:
        print(f"User prompt: {user_prompt}")    
        print(response.text)
        print(f"Prompt tokens: {prompt_tokens}")
        print(f"Response tokens: {response_tokens}")

else:
    response = client.models.generate_content(model="gemini-2.0-flash-001", contents=messages, config=config)
    if response.function_calls:
        for function_call_part in response.function_calls:
            function_call_result = call_function(function_call_part, verbose=False)
            if (
                not function_call_result.parts
                or not function_call_result.parts[0].function_response
            ):
                raise Exception("empty function call result")
            print(f"-> {function_call_result.parts[0].function_response.response}")
    else:    
        print(response.text)




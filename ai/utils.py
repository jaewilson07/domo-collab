import re

def update_function_in_file(file_path, function_name, new_function_str):
    # Read the contents of the file
    with open(file_path, 'r') as file:
        content = file.read()

    # Create a pattern to match the entire function
    pattern = rf'def\s+{function_name}\s*\([^)]*\):.*?(?=\n\S|\Z)'

    # Search for the function in the content
    match = re.search(pattern, content, re.DOTALL)

    if match:
        # If function exists, replace it
        updated_content = content[:match.start()] + new_function_str + content[match.end():]
        
        # Write the updated content back to the file
        with open(file_path, 'w') as file:
            file.write(updated_content)
        
        return f"Function '{function_name}' has been updated in {file_path}"
    else:
        # If function doesn't exist, append the new function to the end of the file
        with open(file_path, 'a') as file:
            file.write('\n\n' + new_function_str)
        
        return f"Function '{function_name}' has been added to {file_path}"

 

# def update_function_in_file(new_function: str, file_path: str = "dataflow.py"):
#     # Read the content of the file
#     with open(file_path, "r") as file:
#         content = file.read()

#     # Extract the function name from the new function
#     function_name = new_function.split("def ")[1].split("(")[0].strip()

#     # Check if the function already exists in the file
#     if f"def {function_name}" in content:
#         # Find the start and end of the existing function
#         start = content.index(f"def {function_name}")
#         end = content.find("\n\n", start)
#         if end == -1:  # If it's the last function in the file
#             end = len(content)
        
#         # Replace the existing function with the new one
#         updated_content = content[:start] + new_function + content[end:]
#     else:
#         # If the function doesn't exist, append it to the end of the file
#         updated_content = content + "\n\n" + new_function

#     # Write the updated content back to the file
#     with open(file_path, "w") as file:
#         file.write(updated_content)

# USER: great now write a function that adds a function to the dataflow.py file if it doesn't exist'
 
import re

# Sample input code
# input_code = """
# ret = requests.post(os.environ['VIDEO_DECODER'], json={"video": base64.b64encode(videoFragment).decode(), "workflow_id": workflow_id, "workflow_depth": workflow_depth + 1, "workflow_width": 0}).text
# result = requests.post(os.environ['VIDEO_RECOG'], json={"frame": base64.b64encode(frame).decode(), "workflow_id": workflow_id, "workflow_depth": workflow_depth + 1, "workflow_width": 0}).text
# """

prefix = 'VIDEO_'
regex = rf"(\w+) = requests.post\(os.environ\['{prefix}(\w+)'\], json=\{{\"(\w+)\": base64.b64encode\((\w+)\).decode\(\), \"workflow_id\": workflow_id, \"workflow_depth\": workflow_depth \+ 1, \"workflow_width\": 0\}}\).text"

def conv(lambda_functions, input_code):
        
    # Perform the replacement
    output_code = re.sub(pattern=regex, repl=replacement, string=input_code)
    # output_code = re.sub(regex, replacement, input_code)

    print("Input code:")
    print(input_code)
    print()

    print("Output code:")
    print(output_code)
    print()





# Function to determine the output function name based on the environment variable
def determine_function_name(env_var):
    return "Decode" if env_var == "VIDEO_DECODER" else "Recognise"

# Replacement function to format the output code
def replacement(match, lambda_functions):
    # all_matches = re.findall(regex, input_code)
    # print('TEMP: ', len(all_matches))
    # print(all_matches)
    variable_name = match.group(1)
    env_var = match.group(2)
    json_key = match.group(3)
    encoded_value = match.group(4)
    function_name = determine_function_name(env_var)
    
    idk = prefix + env_var

    idk = idk.replace('_', '-').lower()

    if idk in lambda_functions:
        print("FOUND A MATCH!", idk)

    # print(f'variable_name: {variable_name}, env_var: {env_var}, json_key: {json_key}, encoded_value: {encoded_value}, function_name: {function_name}')
    return f'{variable_name} = {function_name}({{"{json_key}": base64.b64encode({encoded_value}).decode()}})'

if __name__ == "__main__":
    lambda_functions = ['video-streaming', 'video-decoder', 'video-recog']
    input_code = """
    ret = requests.post(os.environ['VIDEO_DECODER'], json={"video": base64.b64encode(videoFragment).decode(), "workflow_id": workflow_id, "workflow_depth": workflow_depth + 1, "workflow_width": 0}).text
    result = requests.post(os.environ['VIDEO_RECOG'], json={"frame": base64.b64encode(frame).decode(), "workflow_id": workflow_id, "workflow_depth": workflow_depth + 1, "workflow_width": 0}).text
    """
    conv(lambda_functions, input_code)

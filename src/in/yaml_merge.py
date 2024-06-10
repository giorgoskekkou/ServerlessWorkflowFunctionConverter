import os
import yaml
import datetime


def common_prefix(strings):
    return os.path.commonprefix(strings)

def common_suffix(strings):
    reversed_strings = [s[::-1] for s in strings]
    reversed_suffix = os.path.commonprefix(reversed_strings)
    return reversed_suffix[::-1]

def parse_yaml(file_path):
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)
        # return yaml.load(file, Loader=yaml.SafeLoader)
        # return yaml.load(file, Loader=yaml.BaseLoader)
        # return yaml.load(file, Loader=yaml.FullLoader)

def merge_yaml_files(yaml_files):
    merged_yaml = {}
    for key, value in yaml_files.items():
        for k, v in value.items():
            if k not in merged_yaml:
                merged_yaml[k] = [v] if isinstance(v, (str, datetime.datetime)) else v
            else:
                if isinstance(v, (str, datetime.datetime)):
                    v = [v]
                for i in v:
                    if i not in merged_yaml[k]:
                        merged_yaml[k].append(i)
    return merged_yaml

def main():
    directories = []
    yaml_files = {}

    for name in os.listdir('.'):
        if os.path.isdir(name):
            if name not in ['__pycache__', '.git', 'venv', 'build', 'dist', 'requirements', 'requirements.txt', 'requirements_merge.py', 'requirements_merge.sh', 'requirements_merge.bat', 'target']:
                directories.append(name)

                if os.path.exists(name + '/func.yaml'):
                    data = parse_yaml(name + '/func.yaml')
                    yaml_files[name] = data
                
                #     with open(name + '/func.yaml', 'r') as f:
                #         yaml_files[name] = f.read()
                #         for line in f:
                #             line = line.strip('\n')
                #             print(line)

    print("YAML Files: ")
    for key, value in yaml_files.items():
        print("File: ", key)
        print(value)
        print()

    merged_yaml = merge_yaml_files(yaml_files)
    print("Merged YAML: ")
    print(merged_yaml)

    print("Printing all the names")
    for i in range(len(merged_yaml['name'])):
        print(merged_yaml['name'][i])
    print()
    # common_name = os.path.commonprefix(merged_yaml['name'])
    # common_image = os.path.commonprefix(merged_yaml['image'])
    common_name =  common_prefix(merged_yaml['name'])
    common_image = common_prefix(merged_yaml['image'])

    print("Common Name: ", common_name)
    print("Common Image: ", common_image)

    common_name += "full"
    common_image += "full" + common_suffix(merged_yaml['image'])

    # print("SEE HERE: ", common_suffix(merged_yaml['image']))
    merged_yaml['name'] = common_name
    merged_yaml['image'] = common_image

    # Remove the yaml auto generated parts  

    merged_yaml.pop('image')
    merged_yaml.pop('imageDigest')
    merged_yaml.pop('created')

    # merged_yaml.pop('run') # TEMPORARY

    print("Final Merged YAML: ")
    print(merged_yaml)
    print()

    with open('temp.yaml', 'w') as file:
        yaml.dump(merged_yaml, file, default_flow_style=False, sort_keys=False)

main()
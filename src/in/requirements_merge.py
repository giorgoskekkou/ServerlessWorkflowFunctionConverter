# Library imports
import os

# File imports

in_folder = './benchmarks/'

# Functions
def all_strings_same(strings):
    return all(s == strings[0] for s in strings)


def main():
    directories = []
    requirements = {}
    
    
    for name in os.listdir(in_folder):
        if os.path.isdir(in_folder + name):
            if name not in ['__pycache__', '.git', 'venv', 'build', 'dist', 'requirements', 'requirements.txt', 'requirements_merge.py', 'requirements_merge.sh', 'requirements_merge.bat']:
                directories.append(name)

                if os.path.exists(in_folder + name + '/requirements.txt'):
                    with open(in_folder + name + '/requirements.txt', 'r') as f:
                        # requirements[name] = f.read()
                        requirements[name] = []
                        for line in f:
                            if '==' in line:
                                requirement = {
                                    'name': line.split('==')[0], 
                                    'version': line.split('==')[1].strip('\n')
                                }
                            else:
                                requirement = {
                                    'name': line.strip('\n'),
                                    'version': ''
                                }
                            requirements[name].append(requirement)
                            # requirements[name] = line
                            # print(line)
    
    print("Directories: ", directories)
    print("Requirements: ", requirements)

    print()
    # Print the requirments 
    for key, value in requirements.items():
        print("Filename: ", key)
        print("Requirements: ")
        print(value)
        print()
        # print(key, value)
    
    # print("All strings are the same: ", all_strings_same(list(requirements.values())))

    if all_strings_same(list(requirements.values())):
        print("All requirements are the same")
        new_requirements = list(requirements.values())[0]
    else:
        print("Requirements are different")
        new_requirements = {}
        for key, value in requirements.items():
            for requirement in value:
                if requirement['name'] not in new_requirements:
                    new_requirements[requirement['name']] = requirement['version']
                else:
                    if requirement['version'] != '':
                        new_requirements[requirement['name']] = requirement['version']
    
    print("New requirements: ")
    print(new_requirements)
    print()
    
    print("Creating new file: requirements.txt")
    print("--------------------")
    for key, value in new_requirements.items():
        if value != '':
            print(key + '==' + value)
        else:
            print(key)
    print("--------------------")
    
    print() 
        
    # print("Type of requirements: ", type(requirements.values()))
    # Get the current working directory
    # cwd = os.getcwd()
    # print(cwd)

main()
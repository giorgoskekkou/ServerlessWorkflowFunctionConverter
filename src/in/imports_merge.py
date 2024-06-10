# Library imports
import os

def main():
    directories = []
    imports = []
    from_imports = {}

    for name in os.listdir('.'):
        if os.path.isdir(name):
            if name not in ['__pycache__', '.git', 'venv', 'build', 'dist', 'requirements', 'requirements.txt', 'requirements_merge.py', 'requirements_merge.sh', 'requirements_merge.bat']:
                directories.append(name)

                if os.path.exists(name + '/func.py'):
                    with open(name + '/func.py', 'r') as f:
                        for line in f:
                            line = line.strip('\n')
                            if line.startswith('import'):
                                if line not in imports:
                                    imports.append(line)
                            elif line.startswith('from'):
                                line_split = line.split(' ')
                                from_import = {
                                    'from': line_split[1],
                                    'import': line_split[3]
                                }
                                if from_import['from'] not in from_imports:
                                    from_imports[from_import['from']] = []
                                if from_import['import'] not in from_imports[from_import['from']]:
                                    from_imports[from_import['from']].append(from_import['import'])
                                # if line not in from_imports:
                                #     from_imports[line] = []
                                # from_imports[line].append(line)
                            # print(line)

    print("Imports: ", imports)
    print()

    for im in imports:
        print(im)
    print()

    print("From Imports: ", from_imports)
    print()

    print("Start of the file (imports):")
    print("-----------------------------")
    for im in imports:
        print(im)

    for key, value in from_imports.items():
        line = "from " + key + " import "
        for i, v in enumerate(value):
            if i != 0:
                line += ", "
            line += v
        print(line)
    
    print("-----------------------------")
    print()

    # for key, value in from_imports.items():
    #     print("Key: ", key)
    #     for v in value:
    #         print(v)
    #     print()
               






main()


class Node:
    def __init__(self, name):
        self.name = name
        self.children = []
        self.parent = None

    def add_child(self, child):
        self.children.append(child)

    def print_tree(self, level=0):
        print(' ' * level, self.name)
        for child in self.children:
            child.print_tree(level + 1)


def is_function_call(line, function_names):
    stripped_line = line.strip()
    for name in function_names:
        # if name in stripped_line and stripped_line.startswith(name) and not stripped_line.startswith('def'):
        if name in stripped_line:
            return True
    return False
    # return stripped_line.endswith(')') and not stripped_line.startswith('def')

filename = input('Enter the name of the file: ')
node = Node('main')


function_names = []

# open file with code
with open(filename) as file:
    lines = file.readlines()

    # iterate 1st time to get all the function names
    for line in lines:
        if line.startswith('def'):
            function_names.append(line.split('(')[0].split(' ')[1])
    print()
    print(function_names)
    print()

    # iterate 2nd time to get the function calls
    for line in lines:
        if line.strip().startswith('#'):
            continue
        # print(line.strip('\n'))
        if is_function_call(line, function_names):
            node.add_child(Node(line.strip('\n')))

node.print_tree()
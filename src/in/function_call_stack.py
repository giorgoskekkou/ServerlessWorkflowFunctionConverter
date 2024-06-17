
class Node:
    def __init__(self, line, function_name):
        self.line = line
        self.function_name = function_name
        self.children = []
        self.parent = None

    def add_child(self, child):
        self.children.append(child)

    def print_tree(self, level=0):
        print(' ' * level, self.line, ' -> ', self.function_name)
        # print(' ' * level, self.function_name)
        for child in self.children:
            print("Child: ", child.function_name)
            child.print_tree(level + 1)

    def print_tree_with_children(self, level=0):
        for child in self.children:
            if child.function_name == 'main':
                print(child.function_name)
                print(child.children[0])
                # for grandchild in child.children:
                #     print(grandchild.function_name)
                #     print()

def is_function_call(line, function_names):
    stripped_line = line.strip()
    for name in function_names:
        # if name in stripped_line and stripped_line.startswith(name) and not stripped_line.startswith('def'):
        if name in stripped_line:
            return name
    return None
    # return stripped_line.endswith(')') and not stripped_line.startswith('def')

filename = input('Enter the name of the file: ')
# node = Node('main', 'main')
node = Node('root', 'root')


function_names = []
list_of_nodes = []
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
        if line.strip().startswith('#'):    # skip comments
            continue
        # print(line.strip('\n'))
        function_name = is_function_call(line, function_names)
        # if is_function_call(line, function_names):
        if function_name:
            print()
            list_of_nodes.append(Node)
            # node.add_child(Node(line.strip('\n'), function_name))

print("Tree:")
node.print_tree()
print()

print("Tree with children:")
node.print_tree_with_children()
print()

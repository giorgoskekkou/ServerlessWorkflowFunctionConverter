import importlib
import sys

def is_standard_library(module_name):
    """Check if a module is part of the standard library."""
    try:
        module = importlib.import_module(module_name)
        return hasattr(module, '__file__') and 'site-packages' not in module.__file__
    except ImportError:
        # Module not found, could be a typo or not installed if it's third-party.
        return False

def categorize_modules(module_names):
    """Categorize modules into standard library and not."""
    standard_lib = []
    not_standard_lib = []
    
    for name in module_names:
        if is_standard_library(name):
            standard_lib.append(name)
        else:
            not_standard_lib.append(name)
    
    return standard_lib, not_standard_lib

# Example usage
# module_names = ['os', 'sys', 'numpy', 'requests', 'json', 'math']
module_names = ['os', 'sys', 'numpy', 'requests', 'json', 'math', 're', 'selenium', 'yaml']
standard_lib, not_standard_lib = categorize_modules(module_names)

print("Standard Library Modules:", standard_lib)
print("Not Standard Library Modules:", not_standard_lib)
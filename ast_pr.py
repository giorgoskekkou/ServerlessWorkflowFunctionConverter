import ast

class FunctionParamVisitor(ast.NodeVisitor):
	def visit_Call(self, node):
		# Check if the function call is to 'partial'
		if isinstance(node.func, ast.Name) and node.func.id == 'partial':
			# Ensure there is at least one argument
			if node.args:
				# The first argument to 'partial' is the function being partially applied
				func_arg = node.args[0]
				if isinstance(func_arg, ast.Name):
					print(f"Function name passed as parameter: {func_arg.id}")
				elif isinstance(func_arg, ast.Attribute):
					# For methods or attributes, e.g., module.function
					print(f"Function name passed as parameter: {func_arg.attr}")
				# Add more checks here if you're looking for other types of callable, e.g., lambdas
		# Visit other call nodes recursively
		self.generic_visit(node)

# Example source code
source_code = """
ll_result_futures = ex.map(partial(Recognise, workflow_id, workflow_depth), frames)
"""

# Parse the source code into an AST
parsed_code = ast.parse(source_code)

# Create an instance of our visitor and visit the parsed AST
visitor = FunctionParamVisitor()
visitor.visit(parsed_code)
# PYTHON = python3

ifeq ($(OS),Windows_NT)
    PYTHON = python
else
    PYTHON = python3
endif

main:
	$(PYTHON) src/main.py

requirements:
	$(PYTHON) src/modules/requirements_merge.py

imports:
	$(PYTHON) src/modules/imports_merge.py

yaml:
	$(PYTHON) src/modules/yaml_merge.py

function:
	$(PYTHON) src/modules/function_merge.py

# func_call_st:
# 	$(PYTHON) src/in/function_call_stack.py

tree:
	$(PYTHON) src/modules/tree.py

count:
	./count_lines.sh


# PYTHON = python3

ifeq ($(OS),Windows_NT)
    PYTHON = python
else
    PYTHON = python3
endif

main:
	$(PYTHON) src/main.py

requirements:
	$(PYTHON) src/in/requirements_merge.py

imports:
	$(PYTHON) src/in/imports_merge.py

yaml:
	$(PYTHON) src/in/yaml_merge.py

function:
	$(PYTHON) src/in/function_merge.py

func_call_st:
	$(PYTHON) src/in/function_call_stack.py

tree:
	$(PYTHON) src/in/tree.py

count:
	./count_lines.sh


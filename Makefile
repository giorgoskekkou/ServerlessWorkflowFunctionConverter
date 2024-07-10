# PYTHON = python3

ifeq ($(OS),Windows_NT)
    PYTHON = python
else
    PYTHON = python3
endif

main:
	$(PYTHON) src/main.py

requirements:
	$(PYTHON) -m src.modules.requirements_merge
# $(PYTHON) src/modules/requirements_merge.py

imports:
	$(PYTHON) src/modules/imports_merge.py

yaml:
	$(PYTHON) -m src.modules.yaml_merge
# $(PYTHON) src/modules/yaml_merge.py

function:
	$(PYTHON) src/modules/function_merge.py

conv:
	$(PYTHON) src/modules/request_converter.py
# func_call_st:
# 	$(PYTHON) src/in/function_call_stack.py

tree:
	$(PYTHON) -m src.modules.tree

count:
	./count_lines.sh


PYTHON = python3

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

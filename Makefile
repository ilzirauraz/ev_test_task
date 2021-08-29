
lint:
	autoflake --in-place --remove-all-unused-imports --remove-unused-variables -r .
	black . --line-length 79
	isort .

mypy:
	mypy . --config-file setup.cfg --check-untyped-defs

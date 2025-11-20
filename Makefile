.PHONY: setup test run lint clean

setup:
	pip install -r requirements.txt

test:
	python3 -m unittest discover tests

run:
	python3 main.py run

lint:
	# Assuming ruff or pylint. For now, just list files.
	# pip install ruff
	# ruff check .
	@echo "Linting setup pending decision on linter"

clean:
	rm -rf data/

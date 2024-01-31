install:
	pip install --upgrade pip
	pip install -r requirements.txt
format:
	black itsmostdef.../*.py
clean:
	rm -rf dist/ build/ *.egg-info
build:
	python -m build

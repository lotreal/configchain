clean:
	rm -rf build
	rm -rf dist
	rm -rf *.egg-info

update:
	pipenv update
	pipenv lock -r | sed '/^-i/d' | sed '/^--extra-index-url/d' > requirements.txt

build: clean
	python setup.py sdist bdist_wheel

release: build
	python -m twine upload dist/*
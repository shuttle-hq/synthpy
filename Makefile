.PHONY: clean
clean:
	rm -rf dist/
	rm -rf dist/
	rm -rf build/
	rm -rf .eggs/
	find . -name '*.egg-info' -exec rm -rf {} +
	find . -name '*.egg' -exec rm -f {} +

.PHONY: dist
dist: clean
	python setup.py sdist bdist_wheel

.PHONY: dist-upload
dist-upload: dist
	twine upload dist/*

.PHONY: dist-upload-test
dist-upload-test: dist
	twine upload -r testpypi dist/*

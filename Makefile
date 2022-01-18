scope := minor
main_branch_name := master

help: 
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

build: ## Build sdist and bdist_wheel package files.
	python ./setup.py sdist bdist_wheel

clean: ## Clean the contents of the build directories
	rm -rf build/ dist/ *.egg-info 

install:
	python setup.py install

publish: ## Publish the package to Pypi
	twine upload dist/*

test-publish: ## Publish the package to Pypi's test repository
	twine upload --repository testpypi dist/*

test: ## Run unit tests on the code.
	python -m unittest -v

.PHONY: help build clean install publish test-publish test
.DEFAULT_GOAL := help

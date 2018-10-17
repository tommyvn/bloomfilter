test:
	coverage run --source=./bloomfilter -m unittest discover && coverage report -m --skip-covered
	mypy tests bloomfilter
	flake8 tests bloomfilter

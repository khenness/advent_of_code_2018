
all: test run

test:
	pytest -rs -vv --verbose --color=yes code_advent_tests.py


run:
	python code_advent.py

run_debug:
	python code_advent.py "debug"

gitpass:
	git commit -am "WIP - tests pass" ; git push origin master

gitwip:
	git commit -am "Work In Progress" ; git push origin master

pyshell:
	winpty python

run_all: test run

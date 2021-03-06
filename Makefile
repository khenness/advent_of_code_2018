
all: test run

test:
	pytest -rs -vv --verbose --color=yes code_advent_tests.py


run:
	python code_advent.py

run_debug:
	python code_advent.py "debug2"

run_debug_focused:
	python code_advent.py "debug1"

gitpass:
	git commit -am "WIP - tests pass" ; git push origin master

gitwip:
	git commit -am "Work In Progress" ; git push origin master

profile:
	rm ./out.cprof ; python -m cProfile -o out.cprof code_advent.py ; pyprof2calltree -k -i out.cprof


pyshell:
	winpty python

run_all: test run

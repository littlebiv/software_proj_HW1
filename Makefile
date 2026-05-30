.PHONY: all python run-c build-c

all: python

python:
	python3 src/python/kmeans.py 3 100 < data/sample_input.txt

build-c:
	gcc -ansi -Wall -Wextra -Werror -pedantic-errors src/c/kmeans.c -o kmeans -lm

run-c: build-c
	./kmeans 3 100 < data/sample_input.txt

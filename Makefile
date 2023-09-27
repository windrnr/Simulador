default: run
run:
	python3 ./src/test.py ./src/test.csv

compile:
	nuitka3 --standalone --onefile -o Simulador --output-dir=./build ./src/test.py

.PHONY: clean
clean:
	rm -r ./build/*

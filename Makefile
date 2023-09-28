default: run
run:
	python3 ./src/main.py ./src/test.csv

compile:
	nuitka3 --standalone --onefile -o Simulador --output-dir=./build ./src/main.py

.PHONY: clean
clean:
	rm -r ./build/*

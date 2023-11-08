init: 
	pip install -r requirements.txt

run: 
	python3 ./src/main.py 

run_file:
	python3 ./src/main.py ./test/test.csv

compile:
	nuitka3 --standalone --onefile -o Simulador --output-dir=./build ./src/main.py

.PHONY: clean init test
clean:
	rm -r ./build/*

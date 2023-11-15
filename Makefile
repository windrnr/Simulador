init: 
	pip install -r requirements.txt

run: 
	python3 ./src/main.py 

run_file:
	python3 ./src/main.py ./test/test.csv

run_file_step:
	python3 ./src/main.py -f ./test/test.csv

compile:
	python3 -m nuitka --standalone --onefile --show-progress  -o Simulador --output-dir=./build ./src/main.py

.PHONY: clean init test
clean:
	rm -r ./build/*

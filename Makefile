init: 
	pip install -r requirements.txt

run:
	python3 ./simulador/main.py ./test/test.csv

compile:
	nuitka3 --standalone --onefile -o Simulador --output-dir=./build ./sim_mod/main.py

.PHONY: clean init test
clean:
	rm -r ./build/*

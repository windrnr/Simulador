init: 
	pip install -r requirements.txt

run: 
	python3 ./src/main.py 

run_file:
	python3 ./src/main.py ./test/test.csv

run_file_step:
	python3 ./src/main.py -f ./test/test.csv

compile:
	pyinstaller ./src/main.py -F -n "Capybara"

.PHONY: clean init test
clean:
	rm -r ./build/*

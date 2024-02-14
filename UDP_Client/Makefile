.DEFAULT_GOAL := run

setup:
	pip install pyinstaller
run:
	pyinstaller main.py --onefile

clean:
	rmdir build
	rmdir dist
	rm -rf __pycache__

.PHONY:
	run clean

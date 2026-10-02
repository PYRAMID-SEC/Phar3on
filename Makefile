.PHONY: test demo

test:
	python -m unittest discover -s phar3on/tests -t phar3on -v

demo:
	PYTHONPATH=phar3on/src python -m phar3on simulate --scenario all

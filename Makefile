CANDIDATES ?= dataset/candidates.jsonl
OUT       ?= submission.csv

.PHONY: setup model rank validate test clean

setup:
	python -m venv .venv
	.venv/bin/pip install --upgrade pip
	.venv/bin/pip install -r requirements.txt

model:
	python scripts/download_model.py

rank:
	python rank.py --candidates $(CANDIDATES) --out $(OUT)

validate:
	python validate_submission.py $(OUT)

check:
	python scripts/check_output.py $(OUT) $(CANDIDATES)

test:
	python -m pytest tests/ -v

all: rank validate check

clean:
	rm -f submission.csv
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -name "*.pyc" -delete 2>/dev/null || true

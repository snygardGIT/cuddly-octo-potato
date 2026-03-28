.PHONY: run

run:
	./.venv/bin/python -m uvicorn src.app:app --reload --host 0.0.0.0 --port 8000

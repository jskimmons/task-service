.PHONY: setup run test help

help:
	@echo "Available commands:"
	@echo "  run      - Run the application"
	@echo "  test     - Run tests"

run:
	@echo "Running the application..."
	@./start.sh

test:
	@echo "Running included test suite..."
	@./test.sh
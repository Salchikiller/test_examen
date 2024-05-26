.PHONY: run_server run_client test clean test_1 test_1_ok test_2 test_2_ok test_3 test_3_ok

SERVER_PORT=16071

run_server:
	@echo "Starting server on port $(SERVER_PORT)..."
	python3 app/servidor.py $(SERVER_PORT)

run_client:
	@echo "Starting client to connect to server on port $(SERVER_PORT)..."
	python3 app/cliente.py

test:
	@echo "Running all tests..."
	python3 -m unittest discover -s test

clean:
	@echo "Cleaning up..."
	@rm -f *.pyc
	@rm -rf __pycache__

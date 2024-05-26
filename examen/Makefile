.PHONY: run_server run_client test clean

SERVER_PORT=16073

run_server:
	@echo "Starting server on port $(SERVER_PORT)..."
	python3 app/servidor.py $(SERVER_PORT)

run_client:
	@echo "Starting client to connect to server on port $(SERVER_PORT)..."
	python3 app/cliente.py

test: run_server
	@echo "Running tests..."
	python3 test/test_serv.py $(SERVER_PORT)

clean:
	@echo "Cleaning up..."
	@rm -f *.pyc
	@rm -rf __pycache__

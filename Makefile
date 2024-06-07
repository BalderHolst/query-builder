main: build

clean:
	rm -rf build

dev:
	rm -rf build
	make build/query_builder/query.py
	ls ./src/query_builder | xargs -I{} ln $(PWD)/src/query_builder/{} $(PWD)/build/query_builder

build: build/query_builder/query.py
	cp ./src/query_builder/* ./build/query_builder

build/query_builder/query.py: build/query_builder
	./src/generator/generate.py ./src/generator/grammar.dot ./build/query_builder/query.py

build/query_builder:
	mkdir -p build/query_builder


main: build/query_builder

clean:
	rm -rf build

build/query_builder:
	mkdir -p build/query_builder
	cp -v ./src/query_builder/* ./build/query_builder
	python ./src/generator/generate.py ./src/generator/grammar.dot ./build/query_builder/query.py



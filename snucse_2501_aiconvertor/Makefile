dependency-sample-generator:
	poetry run python
		dependency/sample_generator/map_example_project.py \
		data/dependency/sample-project

dependency-map-to-vo-converter:
	poetry run python
		dependency/map_to_vo_converter.py \
		data/dependency/sample-project \
		--vo-class DataVO

build-proworks5-rag:
	poetry run python -m aiconvertor.rag.build_proworks5_rag

analyze-chunks:
	poetry run python -m aiconvertor.rag.analyze_chunks

ask-proworks5:
	poetry run python -m aiconvertor.rag.ask_proworks5

run-convertor-module:
	poetry run python -m aiconvertor.convertor\
		--use-reflextion\
		--iterations 3\
		--mode module\
		--verbose\
		--skip-non-map\
		--use-prompt-normalization\
		-mlo 5\
		--model devstral:24b  

run-convertor-page:
	poetry run python -m aiconvertor.convertor\
		--use-reflextion\
		--iterations 3\
		--mode page\
		--verbose\
		--skip-non-map\
		--use-prompt-normalization\
		-mlo 50\
		--model devstral:24b  

run-convertor-line:
	poetry run python -m aiconvertor.convertor\
		--use-reflextion\
		--iterations 3\
		--mode line\
		--verbose\
		--skip-non-map\
		--use-prompt-normalization\
		-mlo 2\
		--model devstral:24b  

run-vo-generator:
	poetry run python -m aiconvertor.dependency.vo_generator\
		samples/cvt-spring-boot-map/src/ \
		--vo-class DataVO \
		--vo-file samples/cvt-spring-boot-map/cvt-spring-boot-map_vo.java

run:
	poetry run python -m aiconvertor.convertor\
		--use-reflextion\
		--java samples/cvt-spring-boot-map/src/main/java/kds/poc/cvt/service/impl/FundServiceImpl.java\
		--gt samples/cvt-spring-boot/src/main/java/kds/poc/cvt/service/impl/FundServiceImpl.java\
		--context samples/cvt-spring-boot/src/main/java/kds/poc/cvt/model/FundVo.java\
		--mode line\
		--use-api-rag\
		--use-prompt-normalization\
		--skip-non-map\
		-i 3\
		-mlo 1\
		--use-prefix-output\
		--model devstral:24b

		

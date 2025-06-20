install-ts:
	npm install --save-dev typescript

build:
	npm run compile

backend:
	python llm_pipelines.py
IMAGE_NAME ?= swing-options-algo
VERSION ?= 1.0.0
TAG = $(IMAGE_NAME):$(VERSION)
ZIP = Swing-Options-Algo-v$(VERSION).zip

.PHONY: build zip-client

build:
	docker build -t $(TAG) .

zip-client:
	rm -rf tmp_pack || true
	mkdir -p tmp_pack
	cp -r pack tmp_pack/
	cp docker-compose.yml tmp_pack/
	zip -r $(ZIP) tmp_pack/*
	rm -rf tmp_pack

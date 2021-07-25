
IMAGE_NAME ?= "cidash"
REGISTRY ?= "ghcr.io"



build-docker:
	docker build -f docker/Dockerfile -t $(REGISTRY)/$(IMAGE_NAME) .

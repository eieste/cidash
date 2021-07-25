
IMAGE_NAME ?= "cidash/cidash-ui"
REGISTRY ?= "ghcr.io"


build-docker:
	docker build -f docker/Dockerfile -t $(REGISTRY)/$(IMAGE_NAME) .


IMAGE_NAME ?= "cidash/cidash-ui"
REGISTRY ?= "ghcr.io"


build-docker:
	docker build -f docker/Dockerfile --no-cache -t $(REGISTRY)/$(IMAGE_NAME) .

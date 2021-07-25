
IMAGE_NAME ?= "cidash"
REGISTRY ?= "ghcr.io"
ACTOR ?= "eieste"


build-docker:
	docker build -f docker/Dockerfile -t $(REGISTRY)/$(ACTOR)/$(IMAGE_NAME) .

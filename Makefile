# Makefile

# Define variables for Docker image
IMAGE_NAME=your-dockerhub-username/streamlit-rag
TAG=latest

# Install dependencies
.PHONY: install
install:
	pip install -r requirements.txt

# Run tests
.PHONY: test
test:
	pytest

# Build Docker image
.PHONY: docker-build
docker-build:
	docker build -t $(IMAGE_NAME):$(TAG) .

# Push Docker image to DockerHub
.PHONY: docker-push
docker-push: docker-build
	docker push $(IMAGE_NAME):$(TAG)

# Run locally
.PHONY: run-local
run-local:
	streamlit run app.py

# Deploy to server
.PHONY: deploy
deploy:
	ssh -i ~/.ssh/your_server_key.pem user@your_server_ip "\
		docker pull $(IMAGE_NAME):$(TAG) && \
		docker stop streamlit_rag || true && \
		docker rm streamlit_rag || true && \
		docker run -d -p 8501:8501 --name streamlit_rag $(IMAGE_NAME):$(TAG)"

# Full pipeline: install, test, build, push, deploy
.PHONY: all
all: install test docker-push deploy

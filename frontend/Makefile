##########################################################################
# CONFIGURATION
##########################################################################

include env.make
export $(shell sed 's/=.*//' env.make 2>/dev/null)

##########################################################################
# VARIABLES
##########################################################################

PROJECT := qlik
HOME := $(shell echo ~)
PWD := $(shell pwd)
SRC := $(PWD)/src

DOCKER_IMAGE_NAME := $(PROJECT)-frontend
DOCKER_IMAGE_TAG := latest
DOCKER_BUILD_CONTEXT := $(PWD)
DOCKERFILE := $(PWD)/Dockerfile
DOCKER_CONTAINER_NAME := $(DOCKER_IMAGE_NAME)

AZURE_REGISTRY := qlikpalindrom
AZURE_IMAGE_URI := $(AZURE_REGISTRY).azurecr.io/$(DOCKER_IMAGE_NAME):$(DOCKER_IMAGE_TAG)
AZURE_STORAGE_ACCOUNT := qlikpalindrom
AZURE_CONTAINER_NAME := '$$web'

BACKEND_BASE_URL := "https://qlik-backend.orangesky-3031b73d.northeurope.azurecontainerapps.io"

##########################################################################
# CUSTOM MENU
##########################################################################

BLUE      := $(shell tput -Txterm setaf 4)
GREEN     := $(shell tput -Txterm setaf 2)
TURQUOISE := $(shell tput -Txterm setaf 6)
WHITE     := $(shell tput -Txterm setaf 7)
YELLOW    := $(shell tput -Txterm setaf 3)
GREY      := $(shell tput -Txterm setaf 1)
GREY      := $(shell tput -Txterm setaf 1)
SMUL      := $(shell tput smul)
RMUL      := $(shell tput rmul)

HELP_FUN = \
	%help; \
	use Data::Dumper; \
	while(<>) { \
		if (/^([a-zA-Z\-_0-9]+)\s*:.*\#\#(?:@([a-zA-Z\-0-9\.\s]+))?\t(.*)$$/) { \
			$$c = $$2; $$t = $$1; $$d = $$3; \
			push @{$$help{$$c}}, [$$t, $$d, $$ARGV] unless grep { grep { grep /^$$t$$/, $$_->[0] } @{$$help{$$_}} } keys %help; \
		} \
	}; \
	for (sort keys %help) { \
		printf("${WHITE}%24s:${RESET}\n\n", $$_); \
		for (@{$$help{$$_}}) { \
			printf("%s%25s${RESET}%s  %s${RESET}\n", \
				( $$_->[2] eq "Makefile" || $$_->[0] eq "help" ? "${YELLOW}" : "${GREY}"), \
				$$_->[0], \
				( $$_->[2] eq "Makefile" || $$_->[0] eq "help" ? "${GREEN}" : "${GREY}"), \
				$$_->[1] \
			); \
		} \
		print "\n"; \
	}

.DEFAULT_GOAL := help

.PHONY: help
help:: ##@Other	Show this help.
	@echo ""
	@printf "%30s " "${YELLOW}TARGETS"
	@echo "${RESET}"
	@echo ""
	@perl -e '$(HELP_FUN)' $(MAKEFILE_LIST)

##########################################################################
# NPM
##########################################################################

.PHONY: npm-start
npm-start: ##@NPM 	Start React dev server
	npm start

.PHONY: npm-build
npm-build: ##@NPM 	Build React app
	npm run build
	REACT_APP_BACKEND_BASE_URL=$(BACKEND_BASE_URL) npm run build

.PHONY: npm-lint
npm-lint: ##@NPM 	Lint frontend code
	npm run lint

.PHONY: npx-format
npx-format: ##@NPM 	Format frontend code
	npx prettier --write .

##########################################################################
# DOCKER
##########################################################################

.PHONY: docker-build
docker-build: ##@Docker 	Build Docker image for frontend
	docker build -f $(DOCKERFILE) -t $(AZURE_IMAGE_URI) $(DOCKER_BUILD_CONTEXT)

.PHONY: docker-push
docker-push: ##@Docker 	Push frontend image to registry
	docker push $(AZURE_IMAGE_URI)

.PHONY: docker-start
docker-start: docker-stop ##@Docker 	Run frontend container on localhost
	docker run -it --rm --name $(DOCKER_CONTAINER_NAME) -p 3000:80 $(AZURE_IMAGE_URI)

.PHONY: docker-stop
docker-stop: ##@Docker 	Stop and remove frontend container if running
	@docker stop $(DOCKER_CONTAINER_NAME) 2>/dev/null || true

##########################################################################
# AZURE
##########################################################################

.PHONY: azure-upload
azure-upload: ##@Azure 	Build and upload frontend to Azure Static Website
	az storage blob upload-batch \
		--account-name $(AZURE_STORAGE_ACCOUNT) \
		--destination $(AZURE_CONTAINER_NAME) \
		--source build \
		--overwrite

.PHONY: azure-clear
azure-clear: ##@Azure 	Clear current frontend files from Azure Static Website
	az storage blob delete-batch \
		--account-name $(AZURE_STORAGE_ACCOUNT) \
		--source $(AZURE_CONTAINER_NAME)

.PHONY: azure-deploy
azure-deploy: ##@Azure 	Clean and deploy frontend to Azure Static Website
	make npm-build
	make azure-clear
	make azure-upload

.PHONY: azure-url
azure-url: ##@Azure 	Print static website URL for frontend
	@az storage account show \
		--name $(AZURE_STORAGE_ACCOUNT) \
		--query "primaryEndpoints.web" \
		--output tsv

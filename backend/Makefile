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

DOCKER_IMAGE_NAME := $(PROJECT)-backend
DOCKER_IMAGE_TAG := latest
DOCKER_BUILD_CONTEXT := $(PWD)
DOCKERFILE := $(PWD)/Dockerfile
DOCKER_CONTAINER_NAME := $(DOCKER_IMAGE_NAME)

AZURE_RESOURCE_GROUP := qlikpalindrom
AZURE_REGISTRY := qlikpalindrom
AZURE_IMAGE_URI := $(AZURE_REGISTRY).azurecr.io/$(DOCKER_IMAGE_NAME):$(DOCKER_IMAGE_TAG)
AZURE_CONTAINERAPP_NAME := $(PROJECT)-backend

##########################################################################
# CUSTOM MENU
##########################################################################

BLUE      := $(shell tput -Txterm setaf 4)
GREEN     := $(shell tput -Txterm setaf 2)
TURQUOISE := $(shell tput -Txterm setaf 6)
WHITE     := $(shell tput -Txterm setaf 7)
YELLOW    := $(shell tput -Txterm setaf 3)
GREY      := $(shell tput -Txterm setaf 1)
RESET     := $(shell tput -Txterm sgr0)
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

# Variable wrapper
define defw
	custom_vars += $(1)
	$(1) ?= $(2)
	export $(1)
	shell_env += $(1)="$$($(1))"
endef

.PHONY: help
help:: ##@Other 	Show this help.
	@echo ""
	@printf "%30s " "${YELLOW}TARGETS"
	@echo "${RESET}"
	@echo ""
	@perl -e '$(HELP_FUN)' $(MAKEFILE_LIST)

##########################################################################
# PIPENV
##########################################################################

.PHONY: pipenv-install-dev
pipenv-install-dev: ##@Pipenv 	Install all packages including dev dependencies
	pipenv install --dev

.PHONY: pipenv-run
pipenv-run: ##@Pipenv 	Run FastAPI with Uvicorn
	PYTHONPATH=src pipenv run uvicorn src.app.main:app --reload --host 0.0.0.0 --port 8000

.PHONY: pipenv-test
pipenv-test: ##@Pipenv 	Run tests
	pipenv run pytest

.PHONY: pipenv-test-unit
pipenv-test-unit: ##@Pipenv 	Run unit tests only
	pipenv run pytest src/tests/unit

.PHONY: pipenv-test-integration
pipenv-test-integration: ##@Pipenv 	Run integration tests only
	pipenv run pytest src/tests/integration

.PHONY: pipenv-lint
pipenv-lint: ##@Pipenv 	Lint code with flake8
	pipenv run flake8 .

.PHONY: pipenv-black
pipenv-black: ##@Pipenv 	Format code with black
	pipenv run black .

.PHONY: pipenv-shell
pipenv-shell: ##@Pipenv 	Open pipenv shell
	pipenv shell

##########################################################################
# DOCKER
##########################################################################

.PHONY: docker-build
docker-build: ##@Docker 	Build Docker image for backend
	docker build -f $(DOCKERFILE) -t $(AZURE_IMAGE_URI) $(DOCKER_BUILD_CONTEXT)

.PHONY: docker-push
docker-push: ##@Docker 	Push backend image to registry
	docker push $(AZURE_IMAGE_URI)

.PHONY: docker-stop
docker-stop: ##@Docker 	Stop and remove backend container if running
	@docker stop $(DOCKER_CONTAINER_NAME) 2>/dev/null || true
	@docker rm $(DOCKER_CONTAINER_NAME) 2>/dev/null || true

.PHONY: docker-start
docker-start: docker-stop ##@Docker 	Run backend container locally
	docker run -it --rm \
		--name $(DOCKER_CONTAINER_NAME) \
		-p 8000:8000 \
		$(AZURE_IMAGE_URI)

##########################################################################
# AZURE
##########################################################################

.PHONY: azure-acr-login
azure-acr-login: ##@Azure	Log in to Azure Container Registry
	az acr login --name $(AZURE_REGISTRY)

.PHONY: azure-containerapp-update
azure-containerapp-update: ##@Azure 	Update backend Azure Container App with latest image
	az containerapp update \
		--name $(AZURE_CONTAINERAPP_NAME) \
		--resource-group $(AZURE_RESOURCE_GROUP) \
		--image $(AZURE_IMAGE_URI) \
		--set-env-vars RESTART_TRIGGER=$(date +%s)

.PHONY: azure-assign-acr-role
azure-assign-acr-role: ##@Azure 	Assign AcrPull role to Container App for ACR access
	@az role assignment create \
		--assignee $(shell az containerapp show --name $(AZURE_CONTAINERAPP_NAME) --resource-group $(AZURE_RESOURCE_GROUP) --query "identity.principalId" -o tsv) \
		--role "AcrPull" \
		--scope $(shell az acr show --name $(AZURE_REGISTRY) --query "id" -o tsv)

.PHONY: azure-deploy
azure-deploy: ##@Azure 	Deploy backend image to Azure Container App
	make docker-build
	make docker-push
	make azure-containerapp-update

.PHONY: azure-url
azure-url: ##@Azure 	Print backend Container App URL
	@az containerapp show \
		--name $(AZURE_CONTAINERAPP_NAME) \
		--resource-group $(AZURE_RESOURCE_GROUP) \
		--query "properties.configuration.ingress.fqdn" \
		--output tsv

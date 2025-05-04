##########################################################################
# CONFIGURATION
##########################################################################

include env.make
export $(shell sed 's/=.*//' env.make 2>/dev/null)

##########################################################################
# VARIABLES
##########################################################################

HOME := $(shell echo ~)
PWD := $(shell pwd)

##########################################################################
# CUSTOM MENU
##########################################################################

BLUE      := $(shell tput -Txterm setaf 4)
GREEN     := $(shell tput -Txterm setaf 2)
TURQUOISE := $(shell tput -Txterm setaf 6)
WHITE     := $(shell tput -Txterm setaf 7)
YELLOW    := $(shell tput -Txterm setaf 3)
GREY      := $(shell tput -Txterm setaf 1)
RESET     := $(shell tput sgr0)
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
help:: ##@Other Show this help.
	@echo ""
	@printf "%30s " "${YELLOW}TARGETS"
	@echo "${RESET}"
	@echo ""
	@perl -e '$(HELP_FUN)' $(MAKEFILE_LIST)

##########################################################################
# TERRAFORM
##########################################################################

.PHONY: terraform-init
terraform-init: ##@Terraform 	Initialize Terraform
	terraform init

.PHONY: terraform-validate
terraform-validate: ##@Terraform 	Validate Terraform configuration
	terraform validate

.PHONY: terraform-plan
terraform-plan: ##@Terraform 	Show Terraform plan
	terraform plan -var-file=terraform.tfvars

.PHONY: terraform-apply
terraform-apply: ##@Terraform 	Apply Terraform plan
	terraform apply -var-file=terraform.tfvars

.PHONY: terraform-destroy
terraform-destroy: ##@Terraform 	Destroy Terraform-managed resources
	terraform destroy -var-file=terraform.tfvars

.PHONY: terraform-refresh
terraform-refresh: ##@Terraform 	Refresh local state from cloud
	terraform refresh -var-file=terraform.tfvars

.PHONY: terraform-output
terraform-output: ##@Terraform 	Show Terraform outputs
	terraform output

.PHONY: terraform-clean
terraform-clean: ##@Terraform 	Remove local state/cache
	rm -rf .terraform .terraform.lock.hcl terraform.tfstate* crash.log

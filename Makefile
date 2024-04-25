TERRAFORM_SOURCES := $(wildcard terraform/*.tf)
LAMBDA_SOURCES := $(wildcard src/*.py) src/requirements.txt

TERRAFORM_ZIP_NAME := terraform.zip
LAMBDA_ZIP_NAME := lambda.zip

PYTHON := python3.9

# Output directory
DIR := build
TERRAFORM_ZIP := $(DIR)/$(TERRAFORM_ZIP_NAME)
LAMBDA_ZIP := $(DIR)/$(LAMBDA_ZIP_NAME)


.PHONY: clean
clean:
	rm -rf $(DIR)/*

.PHONY: terraform
terraform: $(TERRAFORM_ZIP)
	@echo "Built terraform zip"


$(LAMBDA_ZIP): $(LAMBDA_SOURCES)
	@mkdir -p $(DIR)/lambda
	cp $(LAMBDA_SOURCES) $(DIR)/lambda/
	$(PYTHON) -m pip install \
		--no-compile \
		--no-deps \
		--upgrade \
		--target $(DIR)/lambda/ \
		-r $(DIR)/lambda/requirements.txt
	rm -rf $(DIR)/lambda/*.egg-info $(DIR)/lambda/*.dist-info
	cd $(DIR)/lambda && zip ../$(LAMBDA_ZIP_NAME) -rq *

$(TERRAFORM_ZIP): $(TERRAFORM_SOURCES) $(LAMBDA_ZIP)
	@mkdir -p $(DIR)/terraform
	cp $(LAMBDA_ZIP) $(DIR)/terraform/lambda.zip
	cp $(TERRAFORM_SOURCES) $(DIR)/terraform/
	cd $(DIR)/terraform && zip ../$(TERRAFORM_ZIP_NAME) *

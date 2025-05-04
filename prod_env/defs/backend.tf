terraform {
  backend "azurerm" {
    resource_group_name  = "qlikpalindrom"
    storage_account_name = "qlikpalindrom"
    container_name       = "tfstate"
    key                  = "iac.terraform.tfstate"
  }
}

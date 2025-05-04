variable "subscription_id" {
  description = "Azure subscription ID"
  type        = string
}

variable "location" {
  description = "Azure region"
  type        = string
}

variable "resource_group_name" {
  description = "Azure resource group name"
  type        = string
}

variable "acr_name" {
  description = "Azure Container Registry name (3–50 lowercase alphanumeric)"
  type        = string
}

variable "storage_account_name" {
  description = "Storage Account name (3–24 lowercase letters and numbers)"
  type        = string
}

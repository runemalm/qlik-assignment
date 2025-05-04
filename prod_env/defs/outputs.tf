output "acr_login_server" {
  description = "ACR login server for Docker image push/pull"
  value       = azurerm_container_registry.acr.login_server
}

output "frontend_static_url" {
  description = "Public URL for the React frontend static site"
  value       = azurerm_storage_account.frontend.primary_web_endpoint
}

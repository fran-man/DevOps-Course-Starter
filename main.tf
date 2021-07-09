terraform {
 required_providers {
 azurerm = {
 source = "hashicorp/azurerm"
 version = ">= 2.49"
 }
 }
}
provider "azurerm" {
 features {}
}
data "azurerm_resource_group" "main" {
 name = "AmericanExpress2_GeorgeFrancis_ProjectExercise"
}

resource "azurerm_app_service_plan" "main" {
 name = "george-devops-tf-asp"
 location = data.azurerm_resource_group.main.location
 resource_group_name = data.azurerm_resource_group.main.name
 kind = "Linux"
 reserved = true
 sku {
 tier = "Basic"
 size = "B1"
 }
}
resource "azurerm_app_service" "main" {
 name = "george-devops-terraform"
 location = data.azurerm_resource_group.main.location
 resource_group_name = data.azurerm_resource_group.main.name
 app_service_plan_id = azurerm_app_service_plan.main.id
 site_config {
 app_command_line = ""
 linux_fx_version = "DOCKER|georgefrancis/devops-starter:latest"
 }
 app_settings = {
 "DOCKER_REGISTRY_SERVER_URL" = "https://index.docker.io"
 "MONGO_PASS" = data.azurerm_cosmosdb_account.main.primary_key
 "MONGO_USER" = data.azurerm_cosmosdb_account.main.name
 "OAUTH_ID" = var.OAUTH_ID
 "OAUTH_SECRET" = var.OAUTH_SECRET
 "secret_key" = var.secret_key
 "DOCKER_ENABLE_CI" = var.DOCKER_ENABLE_CI
 "OAUTHLIB_INSECURE_TRANSPORT" = var.OAUTHLIB_INSECURE_TRANSPORT
 "WEBSITES_ENABLE_APP_SERVICE_STORAGE" = var.WEBSITES_ENABLE_APP_SERVICE_STORAGE
 }
}

data "azurerm_cosmosdb_account" "main" {
  name                = "george-devops"
  resource_group_name = data.azurerm_resource_group.main.name
}

resource "azurerm_cosmosdb_mongo_database" "main" {
  name                = "george-devops-tf-mongo"
  resource_group_name = data.azurerm_cosmosdb_account.main.resource_group_name
  account_name        = data.azurerm_cosmosdb_account.main.name
  lifecycle { prevent_destroy = true }
}
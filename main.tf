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
 linux_fx_version = "DOCKER|appsvcsample/python-helloworld:latest"
 }
 app_settings = {
 "DOCKER_REGISTRY_SERVER_URL" = "https://index.docker.io"
 }
}
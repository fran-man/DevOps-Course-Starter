variable "location" {
 description = "The Azure location where all resources in this deployment should be created"
 default = "uksouth"
}

variable "DOCKER_ENABLE_CI" {
 description = "Enable Continuous Integration"
 default = "true"
}

variable "OAUTH_ID" {
 description = "ID for OAUTH authentication"
}

variable "OAUTH_SECRET" {
 description = "Secret for OAUTH authentication"
}

variable "OAUTHLIB_INSECURE_TRANSPORT" {
 description = "Allows OAUTH over HTTP. Should not really be used in prod but ok for this exercise"
 default = 1
}

variable "secret_key" {
 description = "Secret value required by flask"
}

variable "WEBSITES_ENABLE_APP_SERVICE_STORAGE" {
 description = "The Azure location where all resources in this deployment should be created"
 default = "false"
}
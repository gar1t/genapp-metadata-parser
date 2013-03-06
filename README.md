# Metadata Parser for GenApp

This simple Python3 script will parse the metadata into bash-friendly bits.

The data is returned in space-delimited strings.

### Usage
python parser.py FLAG [PARAMS]

### Flags
####{-ls | --list-services}
List all services for the account

####{-lsc | --list-service-config} SERVICE_NAME
List all configuration options for given service

####{-sc | --service-config} SERVICE_NAME CONFIG_OPTION
Get the value associated to the given option for the service

####{-lt | --list-types}
List all resource types available for the application

####{-t | --type} TYPE_NAME
List the resources of the given type that are bound to the app

####{-lrc | --list-resource-config} TYPE_NAME RESOURCE_NAME
Get all configuration options for the given resource and type

####{-rc | --resource-config} TYPE_NAME RESOURCE_NAME CONFIG_OPTION
Get the value for the given option of a resource and type
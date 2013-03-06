#! /usr/local/bin/python

import json
import sys
import os
from pprint import pprint

services = {}
types = {}

def get_metadata():
	json_data=open(os.getenv("app_dir") + "/metadata.json")
	data = json.load(json_data)

	for res in data["app"]["resources"]:
		name = res.get("name", None)
		type = res.get("type", None)
		service = res["service"]
		config = res["config"]

		if type == None:
			services[service] = config

		else:
			if types.get(type, None) == None:
				types[type] = {}

			types[type][name] = config

def print_usage(err):
	print("ERROR: " + err)

	print("--- USAGE ---")
	print("python parser.py FLAG [PARAMS]")

	print("--- FLAGS ---")

	print("{-ls | --list-services}")
	print("\tList all services for the account")

	print("{-lsc | --list-service-config} SERVICE_NAME")
	print("\tList all configuration options for given service")

	print("{-sc | --service-config} SERVICE_NAME CONFIG_OPTION")
	print("\tGet the value associated to the given option for the service")

	print("{-lt | --list-types}")
	print("\tList all resource types available for the application")

	print("{-t | --type} TYPE_NAME")
	print("\tList the resources of the given type that are bound to the app")
	
	print("{-lrc | --list-resource-config} TYPE_NAME RESOURCE_NAME")
	print("\tGet all configuration options for the given resource and type")

	print("{-rc | --resource-config} TYPE_NAME RESOURCE_NAME CONFIG_OPTION")
	print("\tGet the value for the given option of a resource and type")
	sys.exit(1)

def list_services():
	return " ".join(services.keys())

def list_service_config(serv):
	return " ".join(services[serv].keys())

def get_service_config(serv, param):
	return services[serv][param]

def list_types():
	return " ".join(types.keys())

def list_type(type):
	return " ".join(types[type].keys())

def list_resource_config(type, res):
	return " ".join(types[type][res].keys())

def get_resource_config(type, res, param):
	return types[type][res].get(param, "")

if __name__ == "__main__":
	get_metadata()

	if len(sys.argv) > 1:
		arg = sys.argv[1]
		if arg == "-ls" or arg == "--list-services":
			if len(sys.argv) == 2:
				print(list_services())
			else:
				print_usage("This option requires no parameters")

		elif arg == "-lsc" or arg == "--list-service-config":
			if len(sys.argv) == 2:
				print(list_service_config())
			else:
				print_usage("This option requires 1 parameter")

		elif arg == "-sc" or arg == "--service-config":
			if len(sys.argv) == 2:
				print(get_service_config())
			else:
				print_usage("This option requires 2 parameters")

		elif arg == "-lt" or arg == "--list-types":
			if len(sys.argv) == 2:
				print(list_types())
			else:
				print_usage("This option requires no parameters")

		elif arg == "-t" or arg == "--type":
			if len(sys.argv) == 3:
				print(list_type(sys.argv[2]))
			else:
				print_usage("This option requires 1 parameter")

		elif arg == "-lrc" or arg == "--list-resource-config":
			if len(sys.argv) == 4:
				print(list_resource_config(sys.argv[2],sys.argv[3]))
			else:
				print_usage("This option requires 2 parameters")

		elif arg == "-rc" or arg == "--resource-config":
			if len(sys.argv) == 5:
				print(get_resource_config(sys.argv[2],sys.argv[3],sys.argv[4]))
			else:
				print_usage("This option requires 3 parameters")

		else:
			print_usage("Unrecognized option")
	else:
		print_usage("No option given")
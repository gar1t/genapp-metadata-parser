#! /usr/local/bin/python

import json
import sys
import os
import re

services = {}
types = {}
env = {}

def get_metadata():
	json_data=open(os.getenv("genapp_dir") + "/metadata.json")
	data = json.load(json_data)

	for key in data["app"]["env"].keys():
		env[key] = data["app"]["env"][key]

	for res in data["app"]["resources"]:
		name = res.get("name", None)
		type = res.get("type", None)
		service = res["service"]
		config = res["config"]

		if type == None:
			services[service] = config
		else:
			if type == "datasource":
				type = "database"
			if type == "database":
				url = config["DATABASE_URL"]
				db = re.sub(r'.*\/', '', url)
				host = re.sub(r'jdbc:mysql:\/\/', '', url)
				host = re.sub(r':[0-9]*\/%s'%db, '', host)
				port = re.sub('jdbc:mysql:\/\/%s:'%host, '', url)
				port = re.sub(r'\/' + db, '', port)
				config["DATABASE_DB"] = db
				config["DATABASE_HOST"] = host
				config["DATABASE_PORT"] = port
			if types.get(type, None) == None:
				types[type] = {}

			types[type][name] = config


def print_usage(err):
	print("ERROR: " + err)

	print("--- USAGE ---")
	print("python parser.py FLAG [PARAMS]")

	print("--- FLAGS ---")

	print("{-le | --list-environment}")
	print("\tList all environment variables")

	print("{-e | --environment} VARIABLE [DEFAULT]")
	print("\tReturn the given environment variable")

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

def list_env():
	return " ".join(env.keys())

def get_env(var):
	return env[var]

def get_env_def(var, default):
	return env.get(var, default)

def list_services():
	return " ".join(services.keys())

def list_service_config(serv):
	return " ".join(services.get(serv,{}).keys())

def get_service_config(serv, param):
	return services.get(serv,{}).get(param,"")

def list_types():
	return " ".join(types.keys())

def list_type(type):
	return " ".join(types.get(type,{}).keys())

def list_resource_config(type, res):
	return " ".join(types.get(type,{}).get(res, {}).keys())

def get_resource_config(type, res, param):
	return types.get(type,{}).get(res, {}).get(param, "")

if __name__ == "__main__":
	get_metadata()

	if len(sys.argv) > 1:
		arg = sys.argv[1]

		if arg == "-le" or arg == "--list-environment":
			if len(sys.argv) == 2:
				print(list_env())
			else:
				print_usage("This option requires no parameters")

		elif arg == "-e" or arg == "--environment":
			if len(sys.argv) == 3:
				print(get_env(sys.argv[2]))
			elif len(sys.argv) == 4:
				print(get_env_def(sys.argv[2], sys.argv[3]))
			else:
				print_usage("This option requires 1 or 2 parameters")

		elif arg == "-ls" or arg == "--list-services":
			if len(sys.argv) == 2:
				print(list_services())
			else:
				print_usage("This option requires no parameters")

		elif arg == "-lsc" or arg == "--list-service-config":
			if len(sys.argv) == 3:
				print(list_service_config(sys.argv[2]))
			else:
				print_usage("This option requires 1 parameter")

		elif arg == "-sc" or arg == "--service-config":
			if len(sys.argv) == 4:
				print(get_service_config(sys.argv[2], sys.argv[3]))
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
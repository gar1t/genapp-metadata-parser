#! /usr/local/bin/python

from optparse import OptionParser
import json
import sys
import os
import re

metadata = {}

def get_metadata():
    json_data=open(os.getenv("genapp_dir") + "/metadata.json")
    data = json.load(json_data)

    # This loop translates any arrays from the metadata
    # into maps for easier access.
    for key in data.keys():
        val = data[key]
        if key == "app":
            for key2 in val.keys():
                val2 = val[key2]
                if key2 == "resources":
                    services = {}
                    resources = {}
                    for entry in val2:
                        name = entry.get("name", None)
                        if name == None:
                            service = entry["service"]
                            del entry["service"]
                            services[service] = entry
                        else:
                            type = entry["type"]
                            if type == "datasource":
                                type = "database"
                            if type == "database":
                                config = entry["config"]
                                url = config["DATABASE_URL"]
                                db = re.sub(r'.*\/', '', url)
                                host = re.sub(r'^.*mysql:\/\/', '', url)
                                host = re.sub(r':[0-9]*\/%s'%db, '', host)
                                port = re.sub(r'^.*mysql:\/\/%s:'%host, '', url)
                                port = re.sub(r'\/' + db, '', port)
                                config["DATABASE_DB"] = db
                                config["DATABASE_HOST"] = host
                                config["DATABASE_PORT"] = port
                            if resources.get(type, None) == None:
                                resources[type] = {}
                            del entry["name"]
                            resources[type][name] = entry
                else:
                    metadata[key2] = val2
            if services != {}:
                metadata["services"] = services
            if resources != {}:
                metadata["resources"] = resources
        elif key == "plugins":
            plugins = {}
            for entry in val:
                name = entry["name"]
                del entry["name"]
                plugins[name] = entry
            if plugins != {}:
                metadata["plugins"] = plugins
        else:
            metadata[key] = val

def get_values(args, options):
    default = options.default
    current = metadata

    for arg in args:
        if default == None:
            current = current[arg]
        else:
            if isinstance(current, dict):
                current = current.get(arg, default)
            else:
                return default

    if isinstance(current, dict):
        return " ".join(current.keys())
    else:
        return current

if __name__ == "__main__":
    get_metadata()
    
    parser = OptionParser() 
    parser.add_option("-d", "--default", 
        help="Returns default value if search fails")
    (options, args) = parser.parse_args()

    print(get_values(args, options))
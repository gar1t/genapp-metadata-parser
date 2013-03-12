# Metadata Parser for GenApp

This simple Python3 script will parse the metadata into bash-friendly bits
by converting arrays into maps.

The data is returned in space-delimited strings.

## Usage
Requires Python

	./parse key1 key2 key3

## Examples:

	# Gets services activated for this application.
	$ ./parse services
	sendgrid newrelic



	# Gets resource types bound to this application.
	$ ./parse resources
	application email database



	# Gets list of databases bound to this application.
	$ ./parse resources database
	binding1 binding2 binding3



	# Gets configuration keys for the database binding1
	$ ./parse resources database binding1 config
	DATABASE_URL DATABASE_PORT DATABASE_USERNAME DATABASE_PASSWORD DATABASE_HOST 
	DATABASE_DB



	# Gets the database URL:
	$ ./parse resources database binding1 config DATABASE_URL
	mysql://some-domain.amazonaws.com:3306/my_db



	# Get an environment parameter:
	$ ./parse env debug
	true


## License

This work is distributed under the Apache license, found in the LICENSE file.
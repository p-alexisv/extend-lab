# extend-lab

## _CLI tools to help with Support Labs Reservation_

These are python scripts that can help with extending lab reservations or freeing up labs.

1. extend-lab.py
2. free-lab.py


## Requirements
To be able to run these scripts, the following are required in your host machine (Mac or Linux).

1. Python v3
2. Mysql Connector python module


## Download and install the python scripts to your PATH
You could download the python scripts and copy them to your PATH (e.g., /usr/local/bin).  Make sure that they are set as executable.


## Configuration
Each of the scripts has the following lines that need to be updated with the correct information.
```    
dbhost = "DBHOST"
dbuser = "DBUSER"
dbpass = "DBPASS"
```


## Usage
```
$ ./extend-lab.py -h
extend-lab.py -l <lab> -d <domain>
$ ./free-lab.py -h
free-lab.py -l <lab> -d <domain>
$
```



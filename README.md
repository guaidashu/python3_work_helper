If you want to use this small framework. You should follow the steps below.

## Installing and Getting started

1. Clone the repository.

        git clone git@github.com:guaidashu/python3_work_helper.git

2. If there's not a directory which called tool, you must get it. 
   
   For this, you should :
       
       cd template_spider
   
       git clone git@github.com:guaidashu/python3_tool_myself.git
       
       cd python3_tool_myself
       
       mv python3_tool_myself tool

3. Add setting file

    If you use it for the first time, you should create a file called "**secure.py**" in the directory called config which in the root path.
    
    And if you want to use the db. You should input these code in **secure.py**.
        
        INSOMNIA_MUSIC_DATABASE_CONFIG = {
            "MYSQL_DATABASE": "database",
            "MYSQL_USERNAME": "username",
            "MYSQL_PASSWORD": "password",
            "MYSQL_HOST": "localhost",
            "MYSQL_PORT": "3306"
        }
    
    Sure, if you don't want to designate it.
    
    You should config the file called dbconfig.py which in tool/config.

## Usage

None

## FAQ

1. Now, the db class which I write is only support **mysql** and **phoenix** which use to connect **hbase** by python.

## Running Tests

python3 main.py

## Finally Thanks 

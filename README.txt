## Requirements

This is intended to be used with python 3.x  to create a virtualenv please run the following command:

```sh
python3 -m venv venv
source venv/bin/active 
```

Install the requirements by running:  

pip install -r requirements.txt

Once that's complete please run the following to install the discord library.  Currently in beta. 

python3 -m pip install -U "git+https://github.com/Rapptz/discord.py@rewrite#egg=discord.py[voice]"

## Docker integration.

Assuming you have docker and docker compose up and running.

Copy docker_environement.template to docker_environment.  Update the settings as you desire then simply run:

docker-compose up -d and a new MYSQL instance will be created the initial blank slate.



TODO: initial schema required.


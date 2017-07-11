## Requirements

This is intended to be used with python 3.x

To create a virtualenv for encapsulating the setup of the program please run:

```sh
python3 -m venv venv
source venv/bin/activate
```

Install the basic requirements by running:

```sh
pip install -r requirements.txt
```

Once that's complete please run the following to install the discord library as the final requirement. (Note: It's currently in beta.)

```sh
python3 -m pip install -U "git+https://github.com/Rapptz/discord.py@rewrite#egg=discord.py[voice]"
```


## Setup your bot

Please follow the instructions defined [here](https://github.com/reactiflux/discord-irc/wiki/Creating-a-discord-bot-&-getting-a-token) to create your bot in Discord's system and to receive a token for it.

Once you completed them, copy the `config/settings.yaml.template` to `config/settings.yaml` and update it with the token you just got and set the other configurations values.

*Notes on the values:*

- If you want your bot to behave like on the Geek Beacon server, your `prefix` key should have the value `'!n.'`.
- The values in the `startup_cogs` list should be written like the filename of the cogs (without `.py`)

To start the bot simply run:

```sh
python NyaChan.py [dev]
```


## Docker integration

Assuming you have docker and docker compose up and running.

Copy `docker_environement.template` to `docker_environment`.  Update the settings as you desire then simply run:

```sh
docker-compose up -d
```

This will create a new MYSQL instance as the initial blank slate.

TODO: initial schema required.

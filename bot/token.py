from db.readconfig import read_config_params


def get_token():
    try:
        # method will read the env file and return the config object
        params = read_config_params()

        # reading the parameters from the config object
        token = params.get('BOT', 'token')

        return token

    except Exception as error:
        print(error)

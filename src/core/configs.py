

class Config:

    secret_key:str = 'some_secret_key_from_env_var'
    algorithm:str = 'HS256'
    access_token_expire_minutes:int = 60


config = Config()
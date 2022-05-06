import environ

env = environ.Env(expand_vars=True)
base = environ.Path(__file__) - 4
print('-'*50)
print(base)
print('-'*50)
environ.Env.read_env(env_file=base('.env'))

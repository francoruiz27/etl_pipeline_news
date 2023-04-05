import yaml


__config = None


def config():
    global __config
    if not __config:
        with open('/home/franco/proyects/dag/news_proyect/extract/config.yml', mode='r') as f:
            __config = yaml.full_load(f)

    return __config


from .base import *

with open(CONFIG_SECRET_DIR, 'r') as settings_deploy:
    deploy_secret_common_str = settings_deploy.read()

deploy_secret_common = json.loads(deploy_secret_common_str)


DATABASES = deploy_secret_common['django']['databases']

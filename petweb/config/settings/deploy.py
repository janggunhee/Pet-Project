from .base import *

# debug
DEBUG = False

# json filepath 설정
DEPLOY_SECRET = os.path.join(CONFIG_SECRET_DIR, 'settings_deploy.json')
with open(DEPLOY_SECRET, 'r') as settings_deploy:
    deploy_secret_common_str = settings_deploy.read()

deploy_secret_common = json.loads(deploy_secret_common_str)

# databases
DATABASES = deploy_secret_common['django']['databases']

# AWS
AWS_ACCESS_KEY_ID = deploy_secret_common['aws']['access_key_id']
AWS_SECRET_ACCESS_KEY = deploy_secret_common['aws']['secret_access_key']
AWS_STORAGE_BUCKET_NAME = deploy_secret_common['aws']['s3_bucket_name']
AWS_S3_REGION_NAME = deploy_secret_common['aws']['s3-region-name']
AWS_S3_SIGNATURE_VERSION = deploy_secret_common['aws']['s3-signature-version']

# S3 FileStorage
DEFAULT_FILE_STORAGE = 'config.storages.MediaStorage'
STATICFILES_STORAGE = 'config.storages.StaticStorage'

# AWS Storage
STATICFILES_LOCATION = 'static'
MEDIAFILES_LOCATION = 'media'


# AWS elasticbeanstalk HealthCheck
def is_ec2_linux():
    """Detect if we are running on an EC2 Linux Instance
       See http://docs.aws.amazon.com/AWSEC2/latest/UserGuide/identify_ec2_instances.html
    """
    if os.path.isfile("/sys/hypervisor/uuid"):
        with open("/sys/hypervisor/uuid") as f:
            uuid = f.read()
            return uuid.startswith("ec2")
    return False


def get_linux_ec2_private_ip():
    """Get the private IP Address of the machine if running on an EC2 linux server"""
    from urllib.request import urlopen
    if not is_ec2_linux():
        return None
    try:
        response = urlopen('http://169.254.169.254/latest/meta-data/local-ipv4')
        ec2_ip = response.read().decode('utf-8')
        if response:
            response.close()
        return ec2_ip
    except Exception as e:
        print(e)
        return None


private_ip = get_linux_ec2_private_ip()
if private_ip:
    ALLOWED_HOSTS.append(private_ip)

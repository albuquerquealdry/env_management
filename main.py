from cgi import test
from distutils.command.config import config
from distutils.log import error
from types import TracebackType
import yaml
import os
import sys
import json
import base64

def getDefaultEnv():
    envsPreprod = os.popen("""kubectl get secret default-env-preprod -o jsonpath='{.data}' """).read()
    return json.loads(envsPreprod)

def getConfigMap():
    with open("config_map_dev.yaml", 'r') as config_map:
        configMap = yaml.load(config_map)
        return configMap
   
envs = ['HYBRIS_PORT', 'HYBRIS_HOST', 'SOLR_PORT' , 'SOLR_HOST', 'SOLR_SECURE', 'REDIS_PORT', 'REDIS_HOST', 'REDIS_JOAO'  ]
for env in envs:
    configMap = getConfigMap()
    if env in configMap:
        defaultEnvPreprod = getDefaultEnv()
        valueConfigMap = configMap[env]['preprod']
        valueDefault = base64.b64decode(defaultEnvPreprod[env])
        os.system(f"sed -i 's,{valueConfigMap},{valueDefault.decode('utf-8')},g' config_map_dev.yaml ")
    else:
        print(f"NOT FOUND ENV {env}")


dicEnvs = getConfigMap()
envsList = list(getConfigMap())

for env in envsList:   
    try:
        dicEnvs[env]['preprod']
    except KeyError:
        print(f"a env {env} nao existe para preprod")
        dicEnvs[env].apend()

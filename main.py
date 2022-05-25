from cgi import test
from distutils.command.config import config
from distutils.log import error
from types import TracebackType
import yaml
import os
import sys
import json
import base64
import requests

def getVaultKey():
    req = requests.get("http://127.0.0.1:8200/v1/envs/preprod",headers={'X-Vault-Token': 'hvs.2Uf0C9U7M0mPFYICcNarJtha'})
    return req.content

def getConfigMap():
     with open("config_map_dev.yaml", 'r') as config_map:
         configMap = yaml.load(config_map)
         return configMap
   
envs = ['HYBRIS_PORT', 'HYBRIS_HOST', 'SOLR_PORT' , 'SOLR_HOST', 'SOLR_SECURE', 'REDIS_PORT', 'REDIS_HOST', 'REDIS_JOAO'  ]
for env in envs:
     configMap = getConfigMap()
     if env in configMap:
        defaultEnvPreprod = getVaultKey() 
        dataJsonEnvsDefault = json.loads(defaultEnvPreprod)['data']
        valueConfigMap = configMap[env]['preprod']
        valueDefault = dataJsonEnvsDefault[env]

        os.system(f"sed -i 's,{valueConfigMap},{valueDefault},g' config_map_dev.yaml ")
     else:
         print(f"NOT FOUND ENV {env}")


# dicEnvs = getConfigMap()
# envsList = list(getConfigMap())

# for env in envsList:   
#      try:
#          dicEnvs[env]['preprod']
#      except KeyError:
#          print(f"a env {env} nao existe para preprod")
#          dicEnvs[env].apend()

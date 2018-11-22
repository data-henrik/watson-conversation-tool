import json
import ibm_db
from watson_developer_cloud import DiscoveryV1


def handleClientActions(context, actions, watsonResponse):
    print (">>> processing client actions...\n")

    context['skills']['main skill']['user_defined'].update({'mydateOUT':'2018-10-08'})
    print (json.dumps(actions))
    return context
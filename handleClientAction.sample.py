# sample file showing function stub to process client actions

import json

def handleClientActions(context, actions):
    print(">>> processing client actions")
    context.update({'mydateOUT':'2018-10-08'})
    print (json.dumps(actions))
    return context
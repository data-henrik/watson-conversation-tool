# sample file showing function stub to process client actions

import json

# The current context, the action array and the entire response from Watson Assistant
# are passed in. The response contains the context and the actions, but they are
# provided as parameters for convenience.
def handleClientActions(context, actions, watsonResponse):
    print(">>> processing client actions")
    context.update({'mydateOUT':'2018-10-08'})
    print (json.dumps(actions))
    return context
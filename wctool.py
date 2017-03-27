# Manage workspaces for IBM Watson Conversation service on Bluemix
#
# This is a simple Python script to manage Conversation workspaces.
# See the README for details.
#
# Author: Henrik Loeser

import json, argparse
from os.path import join, dirname
from watson_developer_cloud import ConversationV1

# Credentials are read from a file
with open("config.json") as confFile:
     config=json.load(confFile)['credentials']

# Initialize the Conversation client
conversation = ConversationV1(
    username=config['username'],
    password=config['password'],
    version=config['version']
    )


# Define parameters that we want to catch and some basic command help
def getParameters(args=None):
    parser = argparse.ArgumentParser(description='Process my Watson Conversation Commands',prog='wc-client')
    parser.add_argument("--list", "-l",dest='listWorkspaces', action='store_true', help='--list')
    parser.add_argument("--get", "-g",dest='getWorkspace', action='store_true', help='--get')
    parser.add_argument("-export",dest='exportWorkspace', action='store_true', help='export the workspace')
    parser.add_argument("-id",dest='workspaceID', help='Workspace ID')
    parms = parser.parse_args()
    return parms

# List available dialogs
def listWorkspaces():
    print(json.dumps(conversation.list_workspaces(), indent=2))

# Get a specific workspaceID
def getWorkspace(workspaceID,exportWS):
    print(json.dumps(conversation.get_workspace(workspace_id=workspaceID,export=exportWS), indent=2))

#
# Main program, for now just detect what function to call and invoke it
#
if __name__ == '__main__':
    parms = getParameters()
    print parms
    if (parms.registerDialog and parms.dialogFile):
       registerDialog(parms.dialogFile,parms.dialogName)
    if (parms.listWorkspaces):
       listWorkspaces()
    if (parms.getWorkspace and parms.workspaceID):
        getWorkspace(parms.workspaceID,exportWS=parms.exportWorkspace)

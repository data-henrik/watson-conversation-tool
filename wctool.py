# Copyright 2017 IBM Corp. All Rights Reserved.
# See LICENSE for details.
#
# Author: Henrik Loeser
#
# Manage workspaces for IBM Watson Conversation service on IBM Bluemix.
# See the README for documentation.
#

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
    parser = argparse.ArgumentParser(description='Process my Watson Conversation Commands',prog='wctool')
    parser.add_argument("-l",dest='listWorkspaces', action='store_true', help='list workspaces')
    parser.add_argument("-g",dest='getWorkspace', action='store_true', help='get details for single workspace')
    parser.add_argument("-full",dest='fullWorkspace', action='store_true', help='get the full workspace')
    parser.add_argument("-id",dest='workspaceID', help='Workspace ID')
    parser.add_argument("-o",dest='outFile', help='Workspace ID')

    parms = parser.parse_args()
    return parms

# List available dialogs
def listWorkspaces():
    print(json.dumps(conversation.list_workspaces(), indent=2))

# Get and print a specific workspace by ID
def getPrintWorkspace(workspaceID,exportWS):
    print(json.dumps(conversation.get_workspace(workspace_id=workspaceID,export=exportWS), indent=2))

# Get a specific workspace by ID and export to file
def getSaveWorkspace(workspaceID,outFile):
    ws=conversation.get_workspace(workspace_id=workspaceID,export=True)
    with open(outFile,'w') as jsonFile:
        json.dump(ws, jsonFile, indent=2)
    print "Document saved to " + outFile


#
# Main program, for now just detect what function to call and invoke it
#
if __name__ == '__main__':
    parms = getParameters()
    print parms
    if (parms.listWorkspaces):
        listWorkspaces()
    if (parms.getWorkspace and parms.workspaceID):
        if (parms.outFile):
            getSaveWorkspace(parms.workspaceID,parms.outFile)
        else:
            getPrintWorkspace(parms.workspaceID,exportWS=parms.fullWorkspace)

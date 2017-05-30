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
    version=config['version'],
    url=config['url']
    )


# Define parameters that we want to catch and some basic command help
def getParameters(args=None):
    parser = argparse.ArgumentParser(description='Manage Watson Conversation workspaces',
                                     prog='wctool.py',
                                     usage='%(prog)s [-h | -l | -g | -c | -u | -d] [options]')
    parser.add_argument("-l",dest='listWorkspaces', action='store_true', help='list workspaces')
    parser.add_argument("-c",dest='createWorkspace', action='store_true', help='create workspace')
    parser.add_argument("-u",dest='updateWorkspace', action='store_true', help='update workspace')
    parser.add_argument("-d",dest='deleteWorkspace', action='store_true', help='delete workspace')
    parser.add_argument("-g",dest='getWorkspace', action='store_true', help='get details for single workspace')
    parser.add_argument("-logs",dest='listLogs', action='store_true', help='list logs')
    parser.add_argument("-dialog",dest='dialog', action='store_true', help='have dialog')
    parser.add_argument("-full",dest='fullWorkspace', action='store_true', help='get the full workspace')
    parser.add_argument("-id",dest='workspaceID', help='Workspace ID')
    parser.add_argument("-o",dest='outFile', help='Workspace Output File')
    parser.add_argument("-i",dest='inFile', help='Workspace Input File')
    parser.add_argument("-name",dest='wsName', help='Workspace Name')
    parser.add_argument("-desc",dest='wsDescription', help='Workspace Description')
    parser.add_argument("-lang",dest='wsLang', help='Workspace Language')
    parser.add_argument("-intents",dest='wsIntents', action='store_true', help='Update Intents')
    parser.add_argument("-entities",dest='wsEntities', action='store_true', help='Update Entities')
    parser.add_argument("-dialog_nodes",dest='wsDialogNodes', action='store_true', help='Update Dialog Nodes')
    parser.add_argument("-counterexamples",dest='wsCounterexamples', action='store_true', help='Update Counterexamples')
    parser.add_argument("-metadata",dest='wsMetadata', action='store_true', help='Update Metadata')

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
    print "Workspace saved to " + outFile


# Update a workspace
# The workspace parts to be updated were specified as command line options
def updateWorkspace(workspaceID,
                    newName=None,
                    newDescription=None,
                    newLang=None,
                    intents=None,
                    entities=None,
                    dialog_nodes=None,
                    counterexamples=None,
                    metadata=None,
                    inFile=None):
    payload = {'intents': None,
                'entities': None,
                'dialog_nodes': None,
                'counterexamples': None,
                'metadata': None}
    # Only read from file if specified
    if (inFile is not None):
        with open(inFile) as jsonFile:
            ws=json.load(jsonFile)
        # Read the sections to be updated
        if intents is not None:
            payload['intents'] = ws['intents']

        if entities is not None:
            payload['entities'] = ws['entities']

        if dialog_nodes is not None:
            payload['dialog_nodes'] = ws['dialog_nodes']

        if counterexamples is not None:
            payload['counterexamples'] = ws['counterexamples']

        if metadata is not None:
            payload['metadata'] = ws['metadata']

    # Now update the workspace
    ws=conversation.update_workspace(workspace_id=workspaceID,
                                    name=newName,
                                    description=newDescription,
                                    language=newLang,
                                    intents=payload['intents'],
                                    entities=payload['entities'],
                                    dialog_nodes=payload['dialog_nodes'],
                                    counterexamples=payload['counterexamples'],
                                    metadata=payload['metadata'])
    print "Workspace updated - new workspace"
    print(json.dumps(ws, indent=2))

# Create a new workspace
def createWorkspace(newName, newDescription, newLang, inFile):
    with open(inFile) as jsonFile:
        ws=json.load(jsonFile)
    newWorkspace=conversation.create_workspace(name=newName,
                                               description=newDescription,
                                               language=newLang,
                                               intents=ws["intents"],
                                               entities=ws["entities"],
                                               dialog_nodes=ws["dialog_nodes"],
                                               counterexamples=ws["counterexamples"],
                                               metadata=ws['metadata'])
    print(json.dumps(newWorkspace, indent=2))

# Delete a workspaceID
def deleteWorkspace(workspaceID):
    conversation.delete_workspace(workspaceID)
    print "Workspace deleted"

# List logs for a specific workspace by ID
# For now just dump them, do not filter, do not store
def listLogs(workspaceID):
    print(json.dumps(conversation.list_logs(workspace_id=workspaceID), indent=2))

# Start a dialog and converse with Watson
def converse(workspaceID):

  print "Starting a conversation, stop by Ctrl+C or saying 'bye'"
  print "======================================================"
  # Start with an empty context object
  context={}

 # Now loop to chat
  while True:
    # get some input
    minput = raw_input("\nPlease enter your input message:\n")
    # if we catch a "bye" then exit
    if (minput == "bye"):
      break
    # send the input to Watson Conversation
    # Set alternate_intents to False for less output
    resp=conversation.message(workspace_id=workspaceID,
                             message_input={'text': minput},
                             alternate_intents=True,
                             context=context,
                             entities=None,
                             intents=None,
                             output=None)

    # Save returned context for next round of conversation
    context=resp['context']

    # Dump the returned answer
    print ""
    print "Full response object:"
    print "---------------------"
    print(json.dumps(resp, indent=2))



#
# Main program, for now just detect what function to call and invoke it
#
if __name__ == '__main__':
    parms = getParameters()
    # enable next line to print parameters
    # print parms
    if (parms.listWorkspaces):
        listWorkspaces()
    if (parms.getWorkspace and parms.workspaceID):
        if (parms.outFile):
            getSaveWorkspace(parms.workspaceID,parms.outFile)
        else:
            getPrintWorkspace(parms.workspaceID,exportWS=parms.fullWorkspace)
    if (parms.updateWorkspace and parms.workspaceID):
        updateWorkspace(parms.workspaceID,
                        parms.wsName,
                        parms.wsDescription,
                        parms.wsLang,
                        parms.wsIntents,
                        parms.wsEntities,
                        parms.wsDialogNodes,
                        parms.wsCounterexamples,
                        parms.wsMetadata,
                        parms.inFile)
    if (parms.createWorkspace and parms.wsName and parms.wsDescription and parms.wsLang and parms.inFile):
        createWorkspace(newName=parms.wsName,
                        newDescription=parms.wsDescription,
                        newLang=parms.wsLang,
                        inFile=parms.inFile)
    if (parms.deleteWorkspace and parms.workspaceID):
        deleteWorkspace(parms.workspaceID)
    if (parms.listLogs and parms.workspaceID):
        listLogs(parms.workspaceID)
    if (parms.dialog and parms.workspaceID):
        converse(parms.workspaceID)

# Copyright 2017-2018 IBM Corp. All Rights Reserved.
# See LICENSE for details.
#
# Author: Henrik Loeser
#
# Manage workspaces for IBM Watson Assistant service on IBM Cloud.
# See the README for documentation.
#

import json, argparse, importlib
from os.path import join, dirname
from ibm_watson import AssistantV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

privcontext=None
assistant=None

def loadAndInit(confFile=None):
    # Credentials are read from a file
    with open(confFile) as confFile:
        config=json.load(confFile)
        configWA=config['credentials']
        if 'ICF_KEY' in config:
            global privcontext
            icf_key=config['ICF_KEY'].split(':')
            privcontext={"private": {"icfcreds": {"user": icf_key[0], "password": icf_key[1]}}}

    # Initialize the Watson Assistant client
    global assistant
    if 'apikey' in configWA:
        # Authentication via IAM
        authenticator = IAMAuthenticator(configWA['apikey'])
        assistant = AssistantV1(
            authenticator=authenticator,
            version=configWA['version'])
        assistant.set_service_url(configWA['url'])
    else:
        print('Apikey for Watson Assistant in credentials.')
        exit


# Define parameters that we want to catch and some basic command help
def initParser(args=None):
    parser = argparse.ArgumentParser(description='Manage Watson Assistant workspaces (skills)',
                                     prog='wctool.py',
                                     usage='%(prog)s [-h | -l | -g | -c | -u | -delete] [options]')
    parser.add_argument("-l",dest='listWorkspaces', action='store_true', help='list workspaces')
    parser.add_argument("-c",dest='createWorkspace', action='store_true', help='create workspace')
    parser.add_argument("-u",dest='updateWorkspace', action='store_true', help='update workspace')
    parser.add_argument("-delete",dest='deleteWorkspace', action='store_true', help='delete workspace')
    parser.add_argument("-g",dest='getWorkspace', action='store_true', help='get details for single workspace')
    parser.add_argument("-logs",dest='listLogs', action='store_true', help='list logs')
    parser.add_argument("-dialog",dest='dialog', action='store_true', help='have dialog')
    parser.add_argument("-outputonly",dest='outputOnly', action='store_true', help='print dialog output only')
    parser.add_argument("-full",dest='fullWorkspace', action='store_true', help='get the full workspace')
    parser.add_argument("-id",dest='workspaceID', help='Workspace ID')
    parser.add_argument("-o",dest='outFile', help='Workspace Output File')
    parser.add_argument("-i",dest='inFile', help='Workspace Input File')
    parser.add_argument("-name",dest='wsName', help='Workspace Name')
    parser.add_argument("-desc",dest='wsDescription', help='Workspace Description')
    parser.add_argument("-lang",dest='wsLang', help='Workspace Language')
    parser.add_argument("-actionmodule",dest='actionModule', help='Module for client action handling')
    parser.add_argument("-filter",dest='filter', help='filter query')
    parser.add_argument("-context",dest='context', help='context file')
    parser.add_argument("-intents",dest='wsIntents', action='store_true', help='Update Intents')
    parser.add_argument("-entities",dest='wsEntities', action='store_true', help='Update Entities')
    parser.add_argument("-dialog_nodes",dest='wsDialogNodes', action='store_true', help='Update Dialog Nodes')
    parser.add_argument("-counterexamples",dest='wsCounterexamples', action='store_true', help='Update Counterexamples')
    parser.add_argument("-metadata",dest='wsMetadata', action='store_true', help='Update Metadata')
    parser.add_argument("-config",dest='confFile', default='config.json', help='configuration file')
    parser.add_argument("-append",dest='append', action='store_true', help='append to or replace workspace')

    return parser

# List available dialogs
def listWorkspaces():
    print(json.dumps(assistant.list_workspaces().get_result(), indent=2))

# Get and print a specific workspace by ID
def getPrintWorkspace(workspaceID,exportWS):
    print(json.dumps(assistant.get_workspace(workspace_id=workspaceID,export=exportWS).get_result(), indent=2))

# Get a specific workspace by ID and export to file
def getSaveWorkspace(workspaceID,outFile):
    ws=assistant.get_workspace(workspace_id=workspaceID,export=True).get_result()
    with open(outFile,'w') as jsonFile:
        json.dump(ws, jsonFile, indent=2)
    print ("Workspace saved to " + outFile)


# Update a workspace
# The workspace parts to be updated were specified as command line options
def updateWorkspace(workspaceID,
                    intents,
                    entities,
                    dialog_nodes,
                    counterexamples,
                    metadata,
                    newName=None,
                    newDescription=None,
                    newLang=None,
                    inFile=None,
                    append=False):
    payload = {'intents': None,
                'entities': None,
                'dialog_nodes': None,
                'counterexamples': None,
                'metadata': None,
                'append': False}
    # Only read from file if specified
    if (inFile is not None):
        with open(inFile) as jsonFile:
            ws=json.load(jsonFile)
        # Read the sections to be updated
        if intents:
            payload['intents'] = ws['intents']

        if entities:
            payload['entities'] = ws['entities']

        if dialog_nodes:
            payload['dialog_nodes'] = ws['dialog_nodes']

        if counterexamples:
            payload['counterexamples'] = ws['counterexamples']

        if metadata:
            payload['metadata'] = ws['metadata']

    # Now update the workspace
    ws=assistant.update_workspace(workspace_id=workspaceID,
                                    name=newName,
                                    description=newDescription,
                                    language=newLang,
                                    intents=payload['intents'],
                                    entities=payload['entities'],
                                    dialog_nodes=payload['dialog_nodes'],
                                    counterexamples=payload['counterexamples'],
                                    metadata=payload['metadata'],
                                    append=append).get_result()
    print ("Workspace updated - new workspace")
    print(json.dumps(ws, indent=2))

# Create a new workspace
def createWorkspace(newName, newDescription, newLang, inFile):
    with open(inFile) as jsonFile:
        ws=json.load(jsonFile)
    newWorkspace=assistant.create_workspace(name=newName,
                                               description=newDescription,
                                               language=newLang,
                                               intents=ws["intents"],
                                               entities=ws["entities"],
                                               dialog_nodes=ws["dialog_nodes"],
                                               counterexamples=ws["counterexamples"],
                                               metadata=ws['metadata']).get_result()
    print(json.dumps(newWorkspace, indent=2))

# Delete a workspaceID
def deleteWorkspace(workspaceID):
    assistant.delete_workspace(workspaceID)
    print ("Workspace deleted")

# List logs for a specific workspace by ID
# For now just dump them, do not filter, do not store
def listLogs(workspaceID, filter):
    print(json.dumps(assistant.list_logs(workspace_id=workspaceID,filter=filter).get_result(), indent=2))

# Start a dialog and converse with Watson
def converse(workspaceID, outputOnly=None, contextFile=None):
  contextFile="session_context.json"
  print ("Starting a conversation, stop by Ctrl+C or saying 'bye'")
  print ("======================================================")
  # Start with an empty context object
  context={}
  first=True

  ## Load conversation context on start or not?
  contextStart = input("Start with empty context? (Y/n)\n")
  if (contextStart == "n" or contextStart == "N"):
      print ("loading old session context...")
      with open(contextFile) as jsonFile:
          context=json.load(jsonFile)
          jsonFile.close()

  # Now loop to chat
  while True:
    # get some input
    minput = input("\nPlease enter your input message:\n")
    # if we catch a "bye" then exit
    if (minput == "bye"):
      break

    # Read the session context from file if we are not entering the loop
    # for the first time
    if not first:
        try:
            with open(contextFile) as jsonFile:
                context=json.load(jsonFile)
        except IOError:
            # do nothing
            print ("ignoring")
        else:
            jsonFile.close()
    else:
        first=False

    # Process IBM Cloud Function credentials if present
    if privcontext is not None:
        context.update(privcontext)

    # send the input to Watson Assistant
    # Set alternate_intents to False for less output
    resp=assistant.message(workspace_id=workspaceID,
                             input={'text': minput},
                             alternate_intents=True,
                             context=context,
                             entities=None,
                             intents=None,
                             output=None).get_result()

    # Save returned context for next round of conversation
    context=resp['context']
    if ('actions' in resp and len(resp['actions']) and resp['actions'][0]['type']=='client'):
        # Dump the returned answer
        if not outputOnly:
            print ("")
            print ("Full response object of intermediate step:")
            print ("------------------------------------------")
            print(json.dumps(resp, indent=2))
        
        if (hca is not None):
            contextNew=hca.handleClientActions(context,resp['actions'], resp)
        
            # call Watson Assistant with result from client action(s)
            resp=assistant.message(workspace_id=workspaceID,
                             input=resp['input'],
                             alternate_intents=True,
                             context=contextNew,
                             entities=resp['entities'],
                             intents=resp['intents'],
                             output=resp['output']).get_result()
            context=resp['context']
        else:
            print("\n\nplease use -actionmodule to define module to handle client actions")
            break


    # Dump the returned answer
    if (outputOnly):
        print ("Response:")
        print(json.dumps(resp["output"]["text"], indent=2))
    else:
        print ("")
        print ("Full response object:")
        print ("---------------------")
        print(json.dumps(resp, indent=2))

    # Persist the current context object to file.
    with open(contextFile,'w') as jsonFile:
        json.dump(context, jsonFile, indent=2)
    jsonFile.close()


#
# Main program, for now just detect what function to call and invoke it
#
if __name__ == '__main__':
    # Assume no module for client actions
    hca=None

    # initialize parser
    parser = initParser()
    parms =  parser.parse_args()

    # enable next line to print parameters
    # print parms

    # load configuration and initialize Watson
    loadAndInit(confFile=parms.confFile)

    if (parms.listWorkspaces):
        listWorkspaces()
    elif (parms.getWorkspace and parms.workspaceID):
        if (parms.outFile):
            getSaveWorkspace(parms.workspaceID,parms.outFile)
        else:
            getPrintWorkspace(parms.workspaceID,exportWS=parms.fullWorkspace)
    elif (parms.updateWorkspace and parms.workspaceID):
        updateWorkspace(parms.workspaceID,
                        parms.wsIntents,
                        parms.wsEntities,
                        parms.wsDialogNodes,
                        parms.wsCounterexamples,
                        parms.wsMetadata,
                        parms.wsName,
                        parms.wsDescription,
                        parms.wsLang,
                        parms.inFile,
                        parms.append)
    elif (parms.createWorkspace and parms.wsName and parms.wsDescription and parms.wsLang and parms.inFile):
        createWorkspace(newName=parms.wsName,
                        newDescription=parms.wsDescription,
                        newLang=parms.wsLang,
                        inFile=parms.inFile)
    elif (parms.deleteWorkspace and parms.workspaceID):
        deleteWorkspace(parms.workspaceID)
    elif (parms.listLogs and parms.workspaceID):
        listLogs(parms.workspaceID,filter=parms.filter)
    elif (parms.dialog and parms.workspaceID):
        if parms.actionModule:
            hca=importlib.import_module(parms.actionModule)
        converse(parms.workspaceID, parms.outputOnly)
    else:
        parser.print_usage()

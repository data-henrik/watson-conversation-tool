# Watson Conversation Tool
The Watson Conversation Tool (wctool) is a Python-based command line tool to manage workspaces of the [IBM Watson Conversation](https://www.ibm.com/watson/developercloud/doc/conversation/index.html) service in IBM Bluemix. It was written to explore the API to manage workspaces.   
Note that to manage workspaces from the command line this tool is not a requirement. The [API provides REST functions](https://www.ibm.com/watson/developercloud/conversation/api/v1/?curl#workspaces) that can be invoked from tools like `curl`.

This project is described in the following blog posts:
* [Manage Your Watson Conversations from the Command Line or App](http://blog.4loeser.net/2017/03/manage-your-watson-conversations-from.html)
* [Watson Conversation: How to Manage Workspaces](https://www.ibm.com/blogs/bluemix/2017/04/watson-conversation-manage-workspaces/)
* [Updates to Chatbot API and Tooling](http://blog.4loeser.net/2017/05/updates-to-chatbot-api-and-tooling.html)

# Overview
The tool consists of a single Python script, `wctool.py`. In order to use it, you need Python and the SDK for the Watson services installed.

If you have been working with the Watson service and Python before, you probably already have everything installed. If not, you need to install Python and then head over to the [Watson Developer Tools](https://www.ibm.com/watson/developercloud/developer-tools.html) and follow the link to the [Python SDK](https://github.com/watson-developer-cloud/python-sdk). Install the SDK, too. Now download a copy of this repository or clone it.   
To use the tool, copy `config.json.sample` to `config.json` and insert your service credentials. Note that the service URL depends on the IBM Bluemix region. It is shown as part of the credentials.

Some commands and parameters:
```
LIST all workspaces:
-l

GET (full) information about a workspace and print or save it
-g -id workspaceID -full       
-g -id workspaceID -o outfile

UPDATE an existing workspace (with optionally intents, entities, etc. read from existing workspace file):
-u -id workspaceID [-name newName] [-lang newLanguage] [-desc newDescription]
  [-intents] [-entities] [-dialog_nodes] [-counterexamples] [-metadata] [-i input-workspace]

DELETE an existing workspace:
-d -id workspaceID

CREATE a new workspace (with intents, entities etc. read from existing workspace file):
-c -name workspace-name -desc workspace-description -lang workspace-language -i input-workspace

List LOGS for a specific workspace with an optional filter string
-logs -id workspaceID -filter filter-string

Have DIALOG using a specific workspace
-dialog -id workspaceID
```

See the included Jupyter Notebook [SampleSession.ipynb](SampleSession.ipynb) for details on how to invoke the commands. Note that in the current state the tool prints out the values for all possible options for debugging purposes. This could be simply disabled in the code. The [filter expressions](https://www.ibm.com/watson/developercloud/doc/conversation/filter-reference.html) are documented as part of the Watson Conversation service.

### Dialog option and contexts
When using the dialog option, the current session context is stored (persisted) in `session_context.json`. It allows to continue a session later on. The file is closed after writing out the current context. After the new message input is obtained from the user, the file `session_context.json` is opened again and its content retrieved. This allows to modify the context object between dialog turns. Context variables can be set, modified or deleted. This includes system variables. Use with caution... :)



# Documentation and Resources
Here are some useful links to documentation and other resources:
* Watson Conversation service: https://www.ibm.com/watson/developercloud/doc/conversation/index.html
* API for Watson Conversation service: https://www.ibm.com/watson/developercloud/conversation/api/v1/#introduction
* Python SDK, Watson Developer Cloud: https://github.com/watson-developer-cloud/python-sdk
* Conversation API file in Python SDK: https://github.com/watson-developer-cloud/python-sdk/blob/master/watson_developer_cloud/conversation_v1.py
* The `argparse` module used for this tool: https://docs.python.org/2/library/argparse.html

# License
See [LICENSE](LICENSE) for license information.

The tool is provided on a "as-is" basis and is un-supported. Use with care...

# Contribute / Contact Information
If you have found errors or some instructions are not working anymore, then please open an GitHub issue or, better, create a pull request with your desired changes.

You can find more tutorials and sample code at:
https://ibm-bluemix.github.io/

# Watson Conversation Tool
The Watson Conversation Tool (wctool) is a Python-based command line tool to manage workspaces of the [IBM Watson Conversation](https://www.ibm.com/watson/developercloud/doc/conversation/index.html) service in IBM Bluemix.

# Overview
To use the tool, copy `config.json.sample` to `config.json` and insert your service credentials.

Some commands and parameters:
```
List all workspaces:
-l

Get (full) information about a workspace and print or save it
-g -id workspaceID -full       
-g -id workspaceID -o outfile

Update an existing workspace:
-u -id workspaceID [-name newName] [-lang newLanguage] [-desc newDescription]

Delete an existing workspace:
-d -id workspaceID

Create a new workspace (with intents, entities etc. read from existing workspace file):
-c -name workspace-name -desc workspace-description -lang workspace-language -i input-workspace
```

# License
See [LICENSE](LICENSE) for license information.

# Contribute / Contact Information
If you have found errors or some instructions are not working anymore, then please open an GitHub issue or, better, create a pull request with your desired changes.

You can find more tutorials and sample code at:
https://ibm-bluemix.github.io/

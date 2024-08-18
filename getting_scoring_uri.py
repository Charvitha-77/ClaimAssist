from azureml.core.webservice import Webservice
from azureml.core.workspace import Workspace

# Connect to your Azure workspace
ws = Workspace.from_config()

# Get the deployed service
service = Webservice(name='lightgbm-service-v3', workspace=ws)

# Get the scoring URI and authentication key
print("Scoring URI: ", service.scoring_uri)
print("API Key: ", service.get_keys())

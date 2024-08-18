import warnings
from cryptography.utils import CryptographyDeprecationWarning

warnings.simplefilter("ignore", CryptographyDeprecationWarning)

from azureml.core.webservice import Webservice
from azureml.core.workspace import Workspace

# Connect to your Azure workspace
ws = Workspace.from_config()

# Retrieve the service
service = Webservice(name='lightgbm-service-v3', workspace=ws)

# Print the logs
logs = service.get_logs()
print(logs)

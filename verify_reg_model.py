import warnings
warnings.filterwarnings(action='ignore', category=DeprecationWarning, module='paramiko')

from azureml.core import Workspace

# Connect to your Azure ML workspace
ws = Workspace.from_config()

# List all models in the workspace
models = ws.models
for name, model in models.items():
    print(f"Name: {name}, Version: {model.version}")


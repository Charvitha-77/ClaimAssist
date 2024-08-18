from azureml.core import Workspace, Model

# Load the workspace from the config file
ws = Workspace.from_config()  # This will read the config.json file in the current directory

# Register the model
model = Model.register(workspace=ws,
                       model_name="Claim_assist_Model_lgbm",  # Name to register the model under
                       model_path="C:/Users/V JAISRI/Downloads/Claim_assist_Model_lgbm.py")  # Local path to the model file

print(f"Model registered: {model.name}, Version: {model.version}")

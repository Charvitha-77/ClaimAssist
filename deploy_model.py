from azureml.core import Workspace, Model
from azureml.core.environment import Environment
from azureml.core.model import InferenceConfig
from azureml.core.webservice import AciWebservice, Webservice

# Connect to workspace
ws = Workspace.from_config()

# Define the environment
env = Environment.from_conda_specification(name="env_name", file_path="conda_dependencies.yml")

# Inference configuration
inference_config = InferenceConfig(entry_script="score.py", environment=env)

# Deployment configuration
deployment_config = AciWebservice.deploy_configuration(cpu_cores=1, memory_gb=1, auth_enabled=True)

# Get the registered model
model = Model(ws, "Claim_assist_Model_lgbm")

# Deploy the model
service = Model.deploy(workspace=ws,
                       name="lightgbm-service-v3",
                       models=[model],
                       inference_config=inference_config,
                       deployment_config=deployment_config)
service.wait_for_deployment(show_output=True)

# Get the scoring URI
print(f"Scoring URI: {service.scoring_uri}")

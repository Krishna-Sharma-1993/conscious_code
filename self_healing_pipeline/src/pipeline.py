#python
import yaml
import time
from retry_manager import retry_build
from mock_service import activate_mock

def run_pipeline(config_file):
    with open(config_file) as f:
        config = yaml.safe_load(f)

    for stage in config['stages']:
        print(f"Running stage: {stage['name']}")
        success = stage['run']()
        if not success:
            print(f"Stage {stage['name']} failed. Retrying...")
            if not retry_build(stage):
                print("Retry failed. Activating mock service...")
                activate_mock(stage['name'])

if __name__ == "__main__":
    run_pipeline("configs/pipeline_config.yaml")


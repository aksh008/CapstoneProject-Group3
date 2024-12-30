import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from harit_model.config.core import config, TRAINED_MODEL_CHECKPOINT 
from harit_model.retrain_pipeline import run_retrain_pipeline
from harit_model.train_pipeline import run_train_pipeline

checkpoint_path = TRAINED_MODEL_CHECKPOINT / config.app_config.clearmlconfig.checkpoint_name
print("check point path: ", checkpoint_path)
if(0 & os.path.exists(checkpoint_path)) :
    print("Running retraining ")
    run_retrain_pipeline()
else:
    print("Running training ")
    run_train_pipeline()

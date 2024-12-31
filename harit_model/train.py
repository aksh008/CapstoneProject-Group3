import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from harit_model.config.core import config, TRAINED_MODEL_CHECKPOINT 
from harit_model.retrain_pipeline import run_retrain_pipeline
from harit_model.train_pipeline import run_train_pipeline
#from harit_model.upload_model  import upload_new_checkpoint
from harit_model.upload_model import upload_files_to_git

if __name__ == "__main__":
    checkpoint_path = TRAINED_MODEL_CHECKPOINT / config.app_config.clearmlconfig.checkpoint_name
    print("check point path: ", checkpoint_path)
    if(os.path.exists(checkpoint_path)) :
        print("Running retraining ")
        run_retrain_pipeline()
    else:
        print("Running training ")
        run_train_pipeline()
        
    #upload_new_checkpoint()
    upload_files_to_git()

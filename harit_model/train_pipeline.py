import sys
import tensorflow as tf
from datetime import datetime
from pathlib import Path
file = Path(__file__).resolve()
parent, root = file.parent, file.parents[1]
sys.path.append(str(root))
from pipeline import parameters

import pandas as pd
import numpy as np
from harit_model.config.core import config
from harit_model.processing.data_manager import load_dataset,save_pipeline
from harit_model.processing.validation import evaluate_model
from harit_model.pipeline import train_mobilenetv2
from harit_model.processing.features import train_test_valid
from harit_model.config.core import TRAINED_MODEL_DIR
from clearml import Task

task = Task.init(project_name='Harit_project_15Dec',task_name='training_task_1')



def run_training() -> None:
    
    """
    Train the model.
    """

    # download and read training data
    path = load_dataset()
    
    #train, test, valid, num classes
    class_indices, train_data, test_data,valid_data,num_classes = train_test_valid(config.app_config.data_dir,
                                                                                    target_size=(224, 224),
                                                                                    batch_size=64)
    model = train_mobilenetv2(num_classes)
    
    logdir = "logs/digits" + datetime.now().strftime("%Y%m%d-%H%M%S")
    callbacks_list = [tf.keras.callbacks.TensorBoard(log_dir=logdir),
                      tf.keras.callbacks.ModelCheckpoint("MyHarit_model_checkpoint.keras",save_best_only=True)]    
    # Train the model
    print("Training the MobileNetV2 model...")
    history = model.fit(train_data,
                    validation_data=valid_data,
                    epochs=parameters['epoch'],
                    callbacks=callbacks_list,
                    batch_size=64)

    test_loss, test_acc = evaluate_model(model,test_data)
    
    # persist trained model
    save_pipeline(model)
    # printing the score
    print(f'Test Accuract:{test_acc},Test loss: {test_loss}' )
    
if __name__ == "__main__":
    run_training()

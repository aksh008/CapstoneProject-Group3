from datetime import datetime
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import tensorflow as tf
from clearml import Task

from harit_model.config.core import TRAINED_MODEL_CHECKPOINT, config
from harit_model.processing.data_manager import load_dataset, save_pipeline
from harit_model.processing.validation import evaluate_model
from harit_model.pipeline import retrain_mobilenetv2
from harit_model.processing.features import train_test_valid
from pipeline import parameters

def run_training() -> None:
    """Train the model."""
    
    # Download dataset
    load_dataset()
    
    # Prepare data
    _, train_data, test_data, valid_data, num_classes = train_test_valid(
        config.app_config.data_dir,
        target_size=(224, 224),
        batch_size=config.model_config.batch_size
    )
    
    # Create and train model
    model = retrain_mobilenetv2(task, num_classes)
    print("Re-training the MobileNetV2 model...")

    logdir = "logs/" + datetime.now().strftime("%Y%m%d-%H%M%S")
    callbacks_list = [
        tf.keras.callbacks.TensorBoard(log_dir=logdir),
        tf.keras.callbacks.ModelCheckpoint(
            TRAINED_MODEL_CHECKPOINT / config.app_config.clearmlconfig.checkpoint_name,
            save_best_only=True
        )    ]    
    
    # Train the model
    model.fit(
        train_data,
        validation_data=valid_data,
        epochs=parameters['epoch'],
        callbacks=callbacks_list,
        batch_size=config.model_config.batch_size
    )

    # Evaluate model
    test_loss, test_acc = evaluate_model(model, test_data)
    
    # Save trained model
    save_pipeline(model)
    
    # Print results
    print(f'Test Accuracy: {test_acc:.4f}, Test Loss: {test_loss:.4f}')

if __name__ == "__main__":
    project_name = config.app_config.clearmlconfig.project_name
    task = Task.init(project_name=project_name, task_name=f"retrain_task_{project_name}")
    task.connect(parameters)
    run_training()
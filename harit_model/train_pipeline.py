import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from harit_model.config.core import config, TRAINED_MODEL_CHECKPOINT
from harit_model.processing.data_manager import load_dataset, save_pipeline
from harit_model.processing.validation import evaluate_model
from harit_model.pipeline import train_mobilenetv2
from harit_model.processing.features import train_test_valid

from clearml import Task
from pipeline import parameters
from datetime import datetime
import tensorflow as tf

def run_training(task) -> None:
    """Train the model."""
    
    print("Invoking load_dataset from datamanager")
    load_dataset()
    
    _, train_data, test_data, valid_data, num_classes = train_test_valid(
        config.app_config.data_dir,
        target_size=(224, 224),
        batch_size=config.model_config.batch_size
    )
    
    model = train_mobilenetv2(num_classes)
    print("Training the MobileNetV2 model...")

    logdir = f"logs/{datetime.now().strftime('%Y%m%d-%H%M%S')}"
    callbacks_list = [
        tf.keras.callbacks.TensorBoard(log_dir=logdir),
        tf.keras.callbacks.ModelCheckpoint(
            TRAINED_MODEL_CHECKPOINT / config.app_config.clearmlconfig.checkpoint_name,
            save_best_only=True
        )
    ]    

    model.fit(
        train_data,
        validation_data=valid_data,
        epochs=parameters['epoch'],
        callbacks=callbacks_list,
        batch_size=config.model_config.batch_size
    )

    test_loss, test_acc = evaluate_model(model, test_data)
    
    save_pipeline(model)
    
    print(f'Test Accuracy: {test_acc:.4f}, Test Loss: {test_loss:.4f}')

def run_train_pipeline() :
    project_name = config.app_config.clearmlconfig.project_name
    task = Task.init(project_name=project_name, task_name=f"train_task_{project_name}")
    task.connect(parameters)
    run_training(task)
    
# if __name__ == "__main__":
#     project_name = config.app_config.clearmlconfig.project_name
#     task = Task.init(project_name=project_name, task_name=f"train_task_{project_name}")
#     task.connect(parameters)
#     run_training()
import sys
from pathlib import Path
file = Path(__file__).resolve()
parent, root = file.parent, file.parents[1]
sys.path.append(str(root))

from harit_model.config.core import config
from harit_model.processing.data_manager import load_dataset, save_pipeline
from harit_model.processing.validation import evaluate_model
from harit_model.pipeline_retrain import train_mobilenetv2
from harit_model.processing.features import train_test_valid

from clearml import Task, OutputModel
from pipeline_retrain import parameters
from datetime import datetime
import tensorflow as tf

task = Task.init(project_name='Harit_project_26Dec',task_name='training_task_26th dec')


# task.set_progress(0)
# task doing stuff
# task.set_progress(50)
# print(task.get_progress())
# task doing more stuff
# task.set_progress(100)

# output_model = OutputModel(task=task, framework="tensorflow")
task.connect(parameters)

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
    model = train_mobilenetv2(num_classes)
    print("Training the MobileNetV2 model...")

    logdir = "logs/digits/" + datetime.now().strftime("%Y%m%d-%H%M%S")
    callbacks_list = [tf.keras.callbacks.TensorBoard(log_dir=logdir),
                      tf.keras.callbacks.ModelCheckpoint("trained_models/Harit_model_checkpoint.keras",save_best_only=True)]    
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
    run_training()
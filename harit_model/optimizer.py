from clearml import Task
from clearml.automation import UniformParameterRange, UniformIntegerParameterRange, DiscreteParameterRange
from clearml.automation import GridSearch, RandomSearch, HyperParameterOptimizer

task = Task.init(
    project_name='Harit_project_25Dec',
    task_name='optimizer_task_25th DEC',
    task_type=Task.TaskTypes.optimizer,
)

optimizer = HyperParameterOptimizer(
      # specifying the task to be optimized, task must be in system already so it can be cloned
      base_task_id="1896685a258f43248f0cf1fc0d50d9ba", 
      # setting the hyperparameters to optimize
      hyper_parameters=[
          # DiscreteParameterRange(name='General/optimizer', values=['adam']),
          UniformParameterRange(name='General/learning_rate', min_value=0.001, max_value=0.003, step_size=0.001),
        #   UniformIntegerParameterRange(name='General/hidden_layers', min_value=1, max_value=3, step_size=1),
        #   UniformIntegerParameterRange(name='General/neurons', min_value=70, max_value=150, step_size=10),
          UniformIntegerParameterRange(name='General/epoch', min_value=1, max_value=3, step_size=1),          
          ],
      # setting the objective metric we want to maximize/minimize
      objective_metric_title='epoch_accuracy',
      objective_metric_series='validation: epoch_accuracy',
      objective_metric_sign='max',

      # setting optimizer
      optimizer_class=RandomSearch,           # SearchStrategy optimizer to use for the hyperparameter search
  
      # configuring optimization parameters
      max_number_of_concurrent_tasks=2,  
      optimization_time_limit=360.,            # The maximum time (in minutes) for the entire optimization process
      execution_queue='default',              # Execution queue to use for launching Tasks
      )


# This will automatically create and print the optimizer new task id for later use.
# If a Task was already created, it will use it.
optimizer.start()

# wait until optimization completes or time-out
optimizer.wait()

# make sure we stop all jobs
optimizer.stop()

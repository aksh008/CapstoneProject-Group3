import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from harit_model.config.core import PACKAGE_ROOT, TRAINED_MODEL_CHECKPOINT, TRAINED_MODEL_DIR, config
from harit_model import __version__ as _version

import git
import os

def upload_new_checkpoint() :
    # Define the repository path and the file to be added
    repo_path = PACKAGE_ROOT
    repo_path = repo_path.parents[0]
    checkpoint_file = TRAINED_MODEL_CHECKPOINT / config.app_config.clearmlconfig.checkpoint_name
    model_h5_file = TRAINED_MODEL_DIR / f"{config.app_config.pipeline_save_file}{_version}.h5"
    
    print("Repo path: ", repo_path)

    # Initialize the repo
    repo = git.Repo(repo_path)

    # Add the file to the repository
    repo.git.add(checkpoint_file)
    repo.git.add(model_h5_file)


    # Commit the changes
    commit_message = 'Add new file to repository'
    repo.index.commit(commit_message)

    # Push the changes to GitHub
    origin = repo.remote(name='origin')

    # For SSH, use:
    origin.push(refspec='main')

    print(f'File {checkpoint_file} pushed to GitHub successfully.')
    print(f'File {model_h5_file} pushed to GitHub successfully.')
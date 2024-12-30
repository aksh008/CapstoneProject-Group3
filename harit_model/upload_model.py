import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from harit_model.config.core import PACKAGE_ROOT, TRAINED_MODEL_CHECKPOINT, config
import git
import os

def upload_new_checkpoint() :
    # Define the repository path and the file to be added
    repo_path = PACKAGE_ROOT
    repo_path = repo_path.parents[0]
    file_path = TRAINED_MODEL_CHECKPOINT / config.app_config.clearmlconfig.checkpoint_name

    print("Repo path: ", repo_path)

    # Initialize the repo
    repo = git.Repo(repo_path)

    # Add the file to the repository
    repo.git.add(file_path)

    # Commit the changes
    commit_message = 'Add new file to repository'
    repo.index.commit(commit_message)

    # Push the changes to GitHub
    origin = repo.remote(name='origin')

    # For SSH, use:
    origin.push(refspec='CICD_test')

    print(f'File {file_path} pushed to GitHub successfully.')
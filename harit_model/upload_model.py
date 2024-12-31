import sys
import os
import subprocess
from dotenv import load_dotenv
from pathlib import Path
import git

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from harit_model.config.core import PACKAGE_ROOT, TRAINED_MODEL_CHECKPOINT, TRAINED_MODEL_DIR, config
from harit_model import __version__ as _version


# Load environment variables
load_dotenv()


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
    origin.push()

    print(f'File {checkpoint_file} pushed to GitHub successfully.')
    print(f'File {model_h5_file} pushed to GitHub successfully.')
    
def upload_files_to_git() :
    try: 
        commit_msg = "commiting keras and h5 files to git"
        gitusername = os.getenv("GIT_USERNAME")
        gitaccesstoken = os.getenv("GIT_PERSONAL_ACCESS_TOKEN")
        git_user_email = os.getenv("GIT_USER_EMAIL")
        print('git email is:', git_user_email)
        print('git username is:', gitusername)
        
        # Define the repository path and the file to be added
        repo_path = PACKAGE_ROOT
        repo_path = repo_path.parents[0]
        
        checkpoint_file = TRAINED_MODEL_CHECKPOINT / config.app_config.clearmlconfig.checkpoint_name
        model_h5_file = TRAINED_MODEL_DIR / f"{config.app_config.pipeline_save_file}{_version}.h5"
        
        # Initialize the git repository
        repo = git.Repo(repo_path)
            

        #SET Git user identity
        print("Configuring Git user identity...")
        subprocess.run(['git', 'config', '--global', 'user.email', git_user_email], cwd=repo_path, check=True)
        subprocess.run(['git', 'config', '--global', 'user.name', gitusername], cwd=repo_path, check=True)
        
        # Get repository URL
        result = subprocess.run(['git', 'remote', 'get-url', 'origin'],capture_output=True, text=True)
        old_url = result.stdout.strip()
        print("old url::", old_url)
            
        # Extract repository path
        repo_name = old_url.split('github.com/')[-1]
        print ("repo path::", repo_name)

        
        # Create new URL with credentials
        new_url = f'https://{gitusername}:{gitaccesstoken}@github.com/{repo_name}'
        print ("new_url::", new_url)
        
        # Update remote URL
        subprocess.run(['git', 'remote', 'set-url', 'origin', new_url])
        print("Authentication completed successfully!")
        
        # git add command
        print ("git add command - adding 2 files")
        print ("checkpoint file:: ",checkpoint_file)
        print ("model h5 file:: ", model_h5_file)
        subprocess.run(['git', 'add', checkpoint_file], cwd=repo_path, check=True),
        subprocess.run(['git', 'add', model_h5_file], cwd=repo_path, check=True)
        
        # git status command
        print ("git status command")
        subprocess.run(['git', 'status'], check=True, text=True)
        
        # Commit the file
        print ("git commit comand")
        subprocess.run(['git', 'commit', '-m', commit_msg], cwd=repo_path, check=True)
                                    
        # Try pushing
        print("Trying to push...")
        result = subprocess.run(['git', 'push'], cwd=repo_path, capture_output=True, text=True)
        if result.returncode == 0:
            print("Push successful!")
        else:
            print(f"Push failed: {result.stderr}")
            
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        print("\nTroubleshooting steps:")
        print("1. Verify your GitHub username")
        print("2. Make sure your Personal Access Token is valid")
        print("3. Check if you have repository access")
        print("4. Verify your internet connection")
    
        
        

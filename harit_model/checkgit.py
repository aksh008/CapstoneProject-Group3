import os
import subprocess
from getpass import getpass
from dotenv import load_dotenv
load_dotenv()

def fix_github_auth():
    
    try:
        commit_msg = "commiting keras file"
        username = os.getenv("GIT_USERNAME")
        token = os.getenv("GIT_PERSONAL_ACCESS_TOKEN")
        
        
        # Get repository URL
        result = subprocess.run(['git', 'remote', 'get-url', 'origin'], 
                              capture_output=True, text=True)
        old_url = result.stdout.strip()
        print("old url::", old_url)
        
        # Extract repository path
        repo_path = old_url.split('github.com/')[-1]
        print ("repo path::", repo_path)
        
        # Create new URL with credentials
        new_url = f'https://{username}:{token}@github.com/{repo_path}'
        print ("new_url", new_url)
        
        # Update remote URL
        subprocess.run(['git', 'remote', 'set-url', 'origin', new_url])
        print("Authentication updated successfully!")
        
        # git add command
        print ("git add command ")
        subprocess.run(['git', 'add', "harit_model/gitpustest1.txt"], check=True)
        
        # Commit the file
        print ("git commit comand")
        subprocess.run(['git', 'commit', '-m', commit_msg], check=True)
                                  
        # Try pushing
        print("Trying to push...")
        result = subprocess.run(['git', 'push'], capture_output=True, text=True)
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

if __name__ == "__main__":
    fix_github_auth()
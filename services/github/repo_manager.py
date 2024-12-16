import os
from flask import jsonify
from github import Github, Auth
import logging

logger = logging.getLogger(__name__)

# Initialize the GitHub client with authentication
def init():
    github_token = os.getenv("GITHUB_TOKEN")
    if not github_token:
        logger.error("GITHUB_TOKEN not set in environment variables.")
        raise EnvironmentError("GITHUB_TOKEN not set in environment variables.")
    
    logger.info("GitHub authentication successful.")
    auth = Auth.Token(github_token)
    return Github(auth=auth)

def get_all_repos():
    try:
        github_client = init()
        user = github_client.get_user()
        repo_names = [repo.name for repo in user.get_repos()]
        
        logger.info(f"Fetched {len(repo_names)} repositories.")
        github_client.close()
        return jsonify({"repositories": repo_names})
    
    except Exception as e:
        logger.exception("Error occurred while fetching repositories.")
        raise

def create_repo(repo_name, is_private=True):
    try:
        github_client = init()
        user = github_client.get_user()
        repo = user.create_repo(repo_name, private=is_private)
        
        logger.info(f"Created new repository: {repo.name}, private: {is_private}")
        github_client.close()
        return jsonify({"repo_name": repo.name})
    
    except Exception as e:
        logger.exception(f"Error occurred while creating repository: {repo_name}.")
        raise

def delete_repo(repo_name):
    try:
        github_client = init()
        user = github_client.get_user()

        # Get the repository and delete it
        repo = user.get_repo(repo_name)
        repo.delete()
        
        logger.info(f"Repository '{repo_name}' deleted successfully.")
        return True  # Return True on successful deletion

    except Exception as e:
        logger.error(f"Error deleting repository '{repo_name}': {e}")
        return False
    finally:
        github_client.close()

if __name__ == "__main__":
    try:
        repos = get_all_repos()
        logger.info(f"Repositories: {repos}")
    except Exception as e:
        logger.error(f"Error: {str(e)}")
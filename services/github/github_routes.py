import logging
from flask import Blueprint, request, jsonify
from .repo_manager import create_repo, get_all_repos, delete_repo

# Set up logging for this module
logger = logging.getLogger(__name__)

github_routes = Blueprint('github_routes', __name__)

@github_routes.route('/repo/create', methods=['POST'])
def create_repo():
    try:
        logger.info("Received request to create a repository.")
        # Parse JSON body
        data = request.get_json()
        if not data:
            logger.warning("Missing request body for create_repo.")
            return jsonify({"error": "Missing request body"}), 400

        repo_name = data.get("name")
        is_private = data.get("is_private")

        # Validate required fields
        if not repo_name or is_private is None:
            logger.warning(f"Invalid input: repo_name={repo_name}, is_private={is_private}")
            return jsonify({"error": "Invalid input. 'name' and 'is_private' are required."}), 400

        # Call the create_repo function
        response = repo_manager.create_repo(repo_name, is_private)
        logger.info(f"Repository '{repo_name}' created successfully.")
        return response, 201

    except Exception as e:
        logger.error(f"Error while creating repository: {str(e)}", exc_info=True)
        return jsonify({"error": str(e)}), 500

@github_routes.route('/repo/get')
def get_all_repos():
    try:
        logger.info("Received request to fetch all repositories.")
        # Call the get_all_repos function
        response = repo_manager.get_all_repos()
        logger.info("Successfully retrieved all repositories.")
        return response, 200

    except Exception as e:
        logger.error(f"Error while fetching repositories: {str(e)}", exc_info=True)
        return jsonify({"error": str(e)}), 500

@github_routes.route('/repo/delete', methods=['DELETE'])
def delete_repo():
    try:
        logger.info("Received request to delete a repository.")
        # Parse JSON body
        data = request.get_json()
        if not data:
            logger.warning("Missing request body for delete_repo.")
            return jsonify({"error": "Missing request body"}), 400

        repo_name = data.get("name")

        # Validate required fields
        if not repo_name:
            logger.warning("Missing 'name' in delete_repo request.")
            return jsonify({"error": "'name' is required."}), 400

        # Call the delete_repo function from repo_manager
        response = repo_manager.delete_repo(repo_name)
        
        if response:
            logger.info(f"Repository '{repo_name}' deleted successfully.")
            return jsonify({"message": f"Repository '{repo_name}' deleted successfully."}), 200
        else:
            logger.error(f"Failed to delete repository '{repo_name}'.")
            return jsonify({"error": "Failed to delete repository."}), 500

    except Exception as e:
        logger.error(f"Error while deleting repository: {str(e)}", exc_info=True)
        return jsonify({"error": str(e)}), 500
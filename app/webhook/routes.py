from flask import request, render_template, Blueprint
from app.extensions import MongoConnect


webhook = Blueprint('webhook', __name__)

# Endpoint for getting POST data from Github

@webhook.route('/receiver', methods=['POST'])
def receiver():
    if request.headers['content_type'] == 'application/json':
        git_post_data = request.json # POST Data from Github
        # Since POST data from Github is different for commit method hence checking for PUSH request
        if git_post_data.get("ref"):
            branch = git_post_data.get("ref")
            action = ["PUSH"] # setting action as PUSH if it is a commit
            request_id = git_post_data["commits"][0]["id"] # for ID
            author = git_post_data["commits"][0]["author"]["name"] # commiter Name
            timestamp = git_post_data["commits"][0]["timestamp"] # Time of the commit
            from_branch = branch[11:] # From branch
            to_branch = from_branch # to branch it will be same in PUSH method
            # Posting the above data in dB using POST method of the above class
            data = {
                'request_id': request_id,
                'author': author,
                'action': action,
                'from_branch': from_branch,
                'to_branch': to_branch,
                'timestamp': timestamp
            }
            obj = MongoConnect(data)
            obj.write(data)
            return {}, 200

        # checking if it is a PULL request, the data is different from the commit method
        elif git_post_data.get("action") == 'opened':
            action = ["PULL"]
            request_id = git_post_data["sender"]["id"]
            author = git_post_data["sender"]["login"]
            timestamp = git_post_data["pull_request"]["updated_at"]
            from_branch = git_post_data["repository"]["default_branch"]
            to_branch = git_post_data["pull_request"]["title"]
            # Posting PULL request data to dB
            data = {
                'request_id': request_id,
                'author': author,
                'action': action,
                'from_branch': from_branch,
                'to_branch': to_branch,
                'timestamp': timestamp
            }
            obj = MongoConnect(data)
            obj.write(data)
            return {}, 200

        # when the action is 'closed' it is MERGE request
        elif git_post_data.get("action") == 'synchronize':
            action = ["MERGE"]
            request_id = git_post_data["sender"]["id"]
            author = git_post_data["sender"]["login"]
            timestamp = git_post_data["pull_request"]["updated_at"]
            from_branch = git_post_data["repository"]["default_branch"]
            to_branch = git_post_data["pull_request"]["title"]
            # Posting MERGE request data to dB
            data = {
                'request_id': request_id,
                'author': author,
                'action': action,
                'from_branch': from_branch,
                'to_branch': to_branch,
                'timestamp': timestamp
            }
            obj = MongoConnect(data)
            obj.write(data)
            return {}, 200
        # The objective is to only check for [PUSH, PULL, MERGE], so escaping other response from Github
        else:
            return {}, 200

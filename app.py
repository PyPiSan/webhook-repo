from flask import Flask, render_template, request, Response
from pymongo import MongoClient
import os

app = Flask(__name__)

# This is to connect to MongoDB database using Pymongo,
class MongoConnect:

    def __init__(self, data):
        conn_str = os.environ["CONN_STRING"] #MongoDB connection string stored in env
        self.client = MongoClient(conn_str)
        cursor = self.client.Webhook #collecting DB
        self.collection = cursor.gitresponse #collecting collection
        self.data = data

# Fetching data from dB, for(GET) method
    def read(self):
        documents = self.collection.find()
        output = [{item: data[item] for item in data if item != '_id'}
                  for data in documents] # escaping MongoDB default id at the response output
        return output

# Wrinting to dB, for (POST) method 
    def write(self, data):
        # log.info('Writing Data')
        new_document = data
        response = self.collection.insert_one(new_document) # using insert_one() method to inset data
        output = {'Status': 'Successfully Inserted'}
        return output

# Homepage view, only fetching of data from dB is allowed,

@app.route('/', methods=['GET'])
def home():
    if request.method == 'GET': 
        data = {}
        obj = MongoConnect(data)
        response = obj.read()
        return render_template('home.html', response=response) # Returning response and rendering template

# Endpoint for getting POST data from Github

@app.route('/payload', methods=['POST'])
def gitaction():
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
            return Response({'Status': 'Successfully Inserted'})

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
            return Response({'Status': 'Successfully Inserted'})

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
            return Response({'Status': 'Successfully Inserted'})
        # The objective is to only check for [PUSH, PULL, MERGE], so escaping other response from Github
        else:
            return Response({'Status': 'No data to write'})

# The host and post is changed to http://localhost:8000
if __name__ == "__main__":
    app.run(debug=True, port=8000, host='0.0.0.0')

from flask import Flask
from flask import request
from gevent.pywsgi import WSGIServer
import git

app = Flask(__name__)


@app.route('/')
def main():
    return "Invalid Request"


@app.route('/<repo_name>', methods=['GET', 'POST'])
def update_repo(repo_name):
    if request.method == 'POST':
        repo_path = "/srv/dev/" + repo_name
        try:
            repo = git.Repo(repo_path)
            repo.git.pull()
            return "Successful"
        except git.errors.NoSuchPathError:
            git.Git().clone("https://github.com/jaeyeun97/"+repo_name+".git", repo_path);
            repo = git.Repo("/srv/dev/"+repo_name)
            repo.git.pull()
            return "New repository Cloned"
    else:
        return "nothing from "+repo

WSGIServer(('', 8000), app).serve_forever()

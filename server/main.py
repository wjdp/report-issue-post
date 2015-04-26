from flask import Flask, jsonify, request, abort
from flask_limiter import Limiter
from crossdomain import crossdomain
from github import Github

from local_settings import *

app = Flask(__name__)
limiter = Limiter(app, global_limits=["30 per day", "10 per hour"])

def github_instance():
  g = Github(GITHUB_TOKEN)
  r = g.get_repo(GITHUB_REPO)
  return r

def github_post_issue(repo, title, page_url, message, name):
  body = """End user submitted issue from page: [{}]({}{})
---

{}

*{}*
""".format(page_url, WEBSITE_URL, page_url, message, name)
  label = repo.get_label(GITHUB_LABEL)
  return repo.create_issue(title=title, body=body, labels=[label])

@app.route("/")
@limiter.exempt
def hello():
  return "Hello World!"

@app.route("/post_issue", methods=['POST', 'OPTIONS'])
@crossdomain(origin='*')
def post_issue():
  if not request.form or not 'title' in request.form:
    return error('Invalid parameters, requires title')
  issue_title = request.form.get('title')
  page_url = request.form.get('page_url')
  message = request.form.get('message')
  name = request.form.get('name')

  repo = github_instance()
  issue = github_post_issue(repo, issue_title, page_url, message, name)

  return jsonify({
    'status': 'success',
    'url': issue.html_url,
  })

def error(title):
  return jsonify({
    'status': 'error',
    'title': title,
  })

if __name__ == "__main__":
  app.debug = True
  app.run(port=59500)

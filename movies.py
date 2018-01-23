import requests
import json
from flask import Flask

app = Flask(__name__)

@app.route('/')
def get_all_open_issues():
    url ="https://api.github.com/orgs/att/repos?type=public"
    response = []
    get_public_repos = requests.get(url)
    public_repos_json = get_public_repos.json()

    for item in public_repos_json:
        repo_issues = requests.get("https://api.github.com/repos/att/"+item['name']+"/issues?state=open").json();
        repo_info = {}
        repo_info['repository name:'] = item['name']
        repo_info['repository_id'] = item['id']
        iss_list = []
        for issue in repo_issues:
            issue_info = {}
            issue_info['issue_id'] = issue['id']
            issue_info['issue_number'] = issue['number']
            issue_info['issue_title'] = issue['title']
            issue_info['issue_description'] = issue['body']
            issue_info['issue_created_at'] = issue['created_at']
            issue_info['issue_created_by_user'] = issue['user']['id']
            issue_info['issue_status'] = issue['state']
            issue_comments = requests.get(issue['comments_url']).json()
            iss_comments = []
            for issue_comment in issue_comments:
                comment = {}
                comment['comment_id'] = issue_comment['id']
                comment['comment_created_at'] = issue_comment['created_at']
                comment['comment_body'] = issue_comment['body']
                comment['comment_user_id'] = issue_comment['user']['id']
                iss_comments.append(comment)
            issue_info['comments'] = iss_comments
            iss_list.append(issue_info)
        repo_info['issues'] = iss_list
        response.append(repo_info)

    print(json.dumps(response, indent=2))
    return response

get_all_open_issues()
if __name__ == '__main__':
    app.run()
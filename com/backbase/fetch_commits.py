import requests
from config import OWNER, REPO, USER, GITHUB_TOKEN

def fetch_commits(owner, repo, user, token=None):
    url = f"https://api.github.com/repos/{owner}/{repo}/commits"
    headers = {'Authorization': f'token {token}'} if token else {}
    params = {'author': user}

    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        commits = response.json()
        for commit in commits:
            sha = commit['sha']
            date = commit['commit']['author']['date']
            message = commit['commit']['message']
            print(f"Commit: {sha}\nDate: {date}\nMessage: {message}\n")
    else:
        print(f"Failed to fetch commits: {response.status_code} {response.text}")

if __name__ == '__main__':
    fetch_commits(OWNER, REPO, USER, GITHUB_TOKEN)

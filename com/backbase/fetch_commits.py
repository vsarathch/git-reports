import requests
import smtplib
from config import OWNER, REPO, USERS, GITHUB_TOKEN
from datetime import datetime, timedelta
from tabulate import tabulate
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Calculate dynamic date range: last 7 days
END_DATE = datetime.utcnow()
START_DATE = END_DATE - timedelta(days=7)

# Convert to ISO 8601 format with 'Z' suffix for UTC
END_DATE_ISO = END_DATE.strftime('%Y-%m-%dT%H:%M:%SZ')
START_DATE_ISO = START_DATE.strftime('%Y-%m-%dT%H:%M:%SZ')

HEADERS = {
    'Accept': 'application/vnd.github+json',
}
if GITHUB_TOKEN:
    HEADERS['Authorization'] = f'token {GITHUB_TOKEN}'

def get_commits(owner, repo, author, since, until):
    url = f'https://api.github.com/repos/{owner}/{repo}/commits'
    params = {
        'author': author,
        'since': since,
        'until': until,
        'per_page': 100,
        'page': 1
    }
    commits = []

    while True:
        response = requests.get(url, headers=HEADERS, params=params)
        if response.status_code != 200:
            print(f"Failed to fetch commits for {author}: {response.status_code} {response.text}")
            return None
        data = response.json()
        if not data:
            break
        commits.extend(data)
        params['page'] += 1
    return commits

def get_commit_details(owner, repo, sha):
    url = f'https://api.github.com/repos/{owner}/{repo}/commits/{sha}'
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def fetch_user_stats(user):
    commits = get_commits(OWNER, REPO, user, START_DATE_ISO, END_DATE_ISO)
    if commits is None:
        return None  # Failed request
    if not commits:
        # No commits in date range
        return {
            'Commits': 0,
            'Files Changed': 0,
            'Lines Added': 0,
            'Lines Deleted': 0
        }

    total_commits = len(commits)
    total_files_changed = 0
    total_additions = 0
    total_deletions = 0

    for commit in commits:
        sha = commit['sha']
        details = get_commit_details(OWNER, REPO, sha)
        if details:
            stats = details.get('stats')
            if stats:
                total_additions += stats.get('additions', 0)
                total_deletions += stats.get('deletions', 0)
            files = details.get('files')
            if files:
                total_files_changed += len(files)

    return {
        'Commits': total_commits,
        'Files Changed': total_files_changed,
        'Lines Added': total_additions,
        'Lines Deleted': total_deletions
    }

def main():
    rows = []
    columns = ['User', 'Commits', 'Files Changed', 'Lines Added', 'Lines Deleted']

    for user in USERS:
        stats = fetch_user_stats(user)
        if stats is None:
            print(f"Could not fetch data for user: {user}")
            continue
        row = [user, stats['Commits'], stats['Files Changed'], stats['Lines Added'], stats['Lines Deleted']]
        rows.append(row)

    print(f"Contribution stats from {START_DATE_ISO} to {END_DATE_ISO} in repo {OWNER}/{REPO}\n")
    results = tabulate(rows, headers=columns, tablefmt='grid')
    print(results)

if __name__ == '__main__':
    main()

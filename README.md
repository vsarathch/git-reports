# GitHub Contribution Report Generator

This project provides a Python script to generate a contribution report for one or more GitHub users within a specified date range. The report includes commit counts, number of files changed, lines added, and lines deleted in a given repository.

---

## Features

- Fetches commits by specified GitHub users in a repository.
- Filters commits based on a dynamic date range (last 7 days by default).
- Retrieves detailed commit statistics including additions, deletions, and files changed.
- Displays contribution data in a clean tabular format.

---

## Prerequisites

- Python 3.6 or higher installed.
- Internet access to reach GitHub API.
- A GitHub Personal Access Token (optional but recommended) for higher rate limits and private repository access.
- Python packages:
    - `requests`
    - `tabulate`

---

## Installation

1. Clone this repository or download the script file.

2. Install required Python packages:



3. (Optional) Generate a GitHub Personal Access Token (PAT) from your GitHub account settings for better API rate limits and access to private repositories.

---

## Configuration

Update the following variables in the Python script before running:

- `OWNER`: GitHub repository owner (e.g., `octocat`).
- `REPO`: Repository name (e.g., `Hello-World`).
- `USERS`: List of GitHub usernames for whom the report should be generated.
- `GITHUB_TOKEN`: Your GitHub Personal Access Token or set to `None` if you want to make unauthenticated requests (limited rate).

The script automatically calculates the date range for the last 7 days relative to the current UTC time.

---

## Usage

Run the script:


The script will output a contribution report in tabular format displaying:

- User
- Commits
- Files Changed
- Lines Added
- Lines Deleted

---

## Example Output

+--------------+----------+---------------+--------------+---------------+

| User | Commits | Files Changed | Lines Added | Lines Deleted |

+--------------+----------+---------------+--------------+---------------+

| github_user1 | 5 | 12 | 150 | 20 |

| github_user2 | 3 | 8 | 95 | 10 |

+--------------+----------+---------------+--------------+---------------+


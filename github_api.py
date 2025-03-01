import requests
import json

def get_repos(user_id):
    if not user_id:
        raise ValueError("User ID cannot be empty")
    
    response = requests.get(f"https://api.github.com/users/{user_id}/repos")
    
    if response.status_code == 200:
        repos = json.loads(response.text)
        return [repo["name"] for repo in repos]
    elif response.status_code == 404:
        raise ValueError(f"GitHub user not found")
    else:
        raise ValueError(f"Error accessing GitHub API")

def get_commits(user_id, repo_name):
    if not user_id or not repo_name:
        raise ValueError("User ID and repo name cannot be empty")
    
    response = requests.get(f"https://api.github.com/repos/{user_id}/{repo_name}/commits")
    
    if response.status_code == 200:
        commits = json.loads(response.text)
        return len(commits)
    elif response.status_code == 404:
        raise ValueError(f"Repository not found")
    else:
        raise ValueError(f"Error accessing GitHub API")

def get_repos_and_commits(user_id):
    repos = get_repos(user_id)
    result = []
    
    for repo in repos:
        try:
            commit_count = get_commits(user_id, repo)
            result.append((repo, commit_count))
        except ValueError:
            result.append((repo, "Error getting commits"))
    
    return result

def print_repos_and_commits(user_id):
    try:
        repos_and_commits = get_repos_and_commits(user_id)
        
        if not repos_and_commits:
            return f"No repositories found"
        
        output = []
        for repo, commit_count in repos_and_commits:
            output.append(f"Repo: {repo} Number of commits: {commit_count}")
        
        return "\n".join(output)
    except ValueError as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":
    user_id = input("Enter GitHub user ID: ")
    print(print_repos_and_commits(user_id))

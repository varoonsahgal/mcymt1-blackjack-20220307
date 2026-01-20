#!/usr/bin/env python3
"""
Script to delete all branches except main using GitHub API
Requires: pip install requests
Usage: python cleanup-branches.py <github_token> <owner> <repo>
Example: python cleanup-branches.py ghp_xxxxx varoonsahgal mcymt1-blackjack-20220307
"""

import sys
import requests

def get_all_branches(owner, repo, token):
    """Get all branches from the repository"""
    url = f"https://api.github.com/repos/{owner}/{repo}/branches"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28"
    }
    
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

def delete_branch(owner, repo, branch_name, token):
    """Delete a branch from the repository"""
    url = f"https://api.github.com/repos/{owner}/{repo}/git/refs/heads/{branch_name}"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28"
    }
    
    response = requests.delete(url, headers=headers)
    return response.status_code == 204

def main():
    if len(sys.argv) != 4:
        print("Usage: python cleanup-branches.py <github_token> <owner> <repo>")
        print("Example: python cleanup-branches.py ghp_xxxxx varoonsahgal mcymt1-blackjack-20220307")
        sys.exit(1)
    
    token = sys.argv[1]
    owner = sys.argv[2]
    repo = sys.argv[3]
    
    print(f"Fetching branches from {owner}/{repo}...")
    try:
        branches = get_all_branches(owner, repo, token)
    except Exception as e:
        print(f"Error fetching branches: {e}")
        sys.exit(1)
    
    print(f"\nFound {len(branches)} branches:")
    for branch in branches:
        print(f"  - {branch['name']}")
    
    branches_to_delete = [b['name'] for b in branches if b['name'] != 'main']
    
    if not branches_to_delete:
        print("\nNo branches to delete. Only 'main' branch exists.")
        sys.exit(0)
    
    print(f"\nThe following {len(branches_to_delete)} branches will be deleted:")
    for branch_name in branches_to_delete:
        print(f"  - {branch_name}")
    
    confirm = input("\nAre you sure you want to delete these branches? (yes/no): ")
    if confirm.lower() != 'yes':
        print("Operation cancelled.")
        sys.exit(0)
    
    print("\nDeleting branches...")
    deleted = 0
    failed = 0
    
    for branch_name in branches_to_delete:
        print(f"  Deleting: {branch_name}...", end=" ")
        try:
            if delete_branch(owner, repo, branch_name, token):
                print("✓ Deleted")
                deleted += 1
            else:
                print("✗ Failed")
                failed += 1
        except Exception as e:
            print(f"✗ Error: {e}")
            failed += 1
    
    print(f"\nBranch cleanup completed!")
    print(f"  Deleted: {deleted}")
    print(f"  Failed: {failed}")
    
    # Verify remaining branches
    print("\nFetching remaining branches...")
    try:
        remaining_branches = get_all_branches(owner, repo, token)
        print(f"Remaining branches ({len(remaining_branches)}):")
        for branch in remaining_branches:
            print(f"  - {branch['name']}")
    except Exception as e:
        print(f"Error fetching remaining branches: {e}")

if __name__ == "__main__":
    main()

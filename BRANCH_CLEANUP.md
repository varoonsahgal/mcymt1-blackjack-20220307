# Branch Cleanup Guide

This repository includes tools to delete all branches except the `main` branch.

## Current Branches

As of the time this was created, the following branches exist in the repository:
- `main` (will be kept)
- `copilot/improve-slow-code`
- `copilot/refactor-duplicated-code`
- `copilot/remove-all-other-branches`
- `empty-wipe`
- `master`
- `varoonsahgal-patch-1`

## Option 1: Using GitHub Actions (Recommended)

1. Go to the repository on GitHub
2. Click on "Actions" tab
3. Select "Cleanup Branches" workflow from the left sidebar
4. Click "Run workflow" button
5. Confirm and run the workflow
6. The workflow will delete all branches except `main`

## Option 2: Using the Shell Script

If you have local repository access with proper authentication:

```bash
# Make sure you're in the repository directory
cd /path/to/mcymt1-blackjack-20220307

# Run the cleanup script
./cleanup-branches.sh
```

The script will:
1. List all branches that will be deleted
2. Ask for confirmation
3. Delete all branches except `main`

## Option 3: Manual Deletion

You can manually delete branches using git commands:

```bash
# Delete a single branch
git push origin --delete <branch-name>

# Example:
git push origin --delete copilot/improve-slow-code
git push origin --delete copilot/refactor-duplicated-code
git push origin --delete empty-wipe
git push origin --delete master
git push origin --delete varoonsahgal-patch-1
```

## Note

After running any of these cleanup methods, only the `main` branch will remain in the repository.

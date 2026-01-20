#!/bin/bash

# Script to delete all branches except main
# This script requires proper GitHub authentication (gh CLI or git credentials)

set -e

echo "Fetching all remote branches..."
git fetch --all

echo ""
echo "The following branches will be deleted:"
echo "----------------------------------------"
git ls-remote --heads origin | awk '{print $2}' | sed 's|refs/heads/||' | grep -v '^main$'

echo ""
read -p "Are you sure you want to delete these branches? (yes/no): " confirm

if [ "$confirm" != "yes" ]; then
    echo "Operation cancelled."
    exit 0
fi

echo ""
echo "Deleting branches..."
git ls-remote --heads origin | awk '{print $2}' | sed 's|refs/heads/||' | grep -v '^main$' | while read branch; do
    echo "Deleting: $branch"
    git push origin --delete "$branch" 2>&1 || echo "Failed to delete $branch"
done

echo ""
echo "Branch cleanup completed!"
echo ""
echo "Remaining branches:"
git ls-remote --heads origin

#!/usr/bin/env bash
set -euo pipefail

TARGET_COMMIT="2aa3290c"

if [ ! -d ".git" ]; then
  echo "Error: run this from the repository root (where .git lives)."
  exit 1
fi

echo
echo "***** WARNING *****"
echo "This script will hard-reset 'main' to commit $TARGET_COMMIT and force-push to origin/main."
echo "All commits on main after $TARGET_COMMIT will be removed from main on the remote."
echo "A backup branch of your current state will be created and pushed to origin."
echo "If you are sure, press ENTER to continue, or Ctrl-C to abort."
read -r

TIMESTAMP=$(date +%s)
BACKUP_BRANCH="backup-before-reset-${TIMESTAMP}"
echo
echo "Creating local backup branch: $BACKUP_BRANCH"
git branch "$BACKUP_BRANCH"

echo "Pushing backup branch to origin: $BACKUP_BRANCH"
git push -u origin "$BACKUP_BRANCH"

echo
echo "Fetching origin..."
git fetch origin --prune

echo
echo "Checking out main..."
git checkout main

echo
echo "Verifying target commit exists..."
if ! git cat-file -e "${TARGET_COMMIT}^{commit}"; then
  echo "Error: commit $TARGET_COMMIT not found. Aborting."
  exit 1
fi

echo
echo "Hard resetting local main to $TARGET_COMMIT..."
git reset --hard "$TARGET_COMMIT"

echo
echo "Local main now at:"
git --no-pager log --oneline -n 6

echo
echo "Force-pushing main to origin with --force-with-lease..."
git push --force-with-lease origin main

echo
echo "Done. origin/main now matches commit $TARGET_COMMIT."
echo "If you need to recover the previous state, the backup branch is available at origin/$BACKUP_BRANCH."

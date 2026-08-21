#!/usr/bin/env bash
# Fails when a tracked file regains something that must not be published:
# a home path, or a name identifying the sources the method was exercised on.
# Voir CONTRIBUTING.md, "House rules".
set -uo pipefail
cd "$(dirname "$0")/.."
status=0

if git grep -I --untracked -nE '/Users/[A-Za-z0-9_.-]+|/home/[A-Za-z0-9_.-]+|C:\\\\Users' \
      -- . ':!scripts/check_hygiene.sh' ':!SECURITY.md'; then
  echo "^ absolute home path in a repository file: derive it from the script location instead"
  status=1
fi

# Words that would name the client or the product family the runbooks were written on.
if git grep -I --untracked -niE '(^|[^a-z])(circle|jokon|hella|soverep)([^a-z]|$)' \
      -- . ':!scripts/check_hygiene.sh' | grep -viE 'circle the operator|circular|circle exists|a circle'; then
  echo "^ identifying name in a tracked file"
  status=1
fi

[ $status -eq 0 ] && echo "hygiene: clean"
exit $status

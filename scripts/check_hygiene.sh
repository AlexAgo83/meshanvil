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
# `circle` is also CSS and SVG vocabulary, so it counts only where a name would put it:
# touching an underscore or a hyphen, or capitalised as a word of its own.
if git grep -I --untracked -nE '[Cc]ircle[_-]|CIRCLE[_-]|[_-][Cc]ircle|[_-]CIRCLE|(^|[^A-Za-z])Circle([^a-z]|$)|[Jj]okon|[Hh]ella|[Ss]overep' \
      -- . ':!scripts/check_hygiene.sh'; then
  echo "^ identifying name in a tracked file"
  status=1
fi

[ $status -eq 0 ] && echo "hygiene: clean"
exit $status

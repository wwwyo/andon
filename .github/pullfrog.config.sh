#!/usr/bin/env bash
# Server-side Pullfrog config for wwwyo/andon — this file is the SSOT.
#
# .github/workflows/pullfrog.yml is a Pullfrog-managed file kept pristine
# (byte-identical across repos, updated by upstream PRs). Repo-level settings
# (model, effort, review/issue/label modes, hooks, ...) live in Pullfrog's
# backend and are invisible to git — this script records and reapplies them.
#
# Apply:  .github/pullfrog.config.sh        (uses gh auth)
# Audit:  mise exec -- pullfrog config list --repo wwwyo/andon
#
# Model and its auth are per owner (anthropic: keyless OIDC / opencode-go: OPENCODE_API_KEY)
# — see model_for in .github/pullfrog.org.config.sh (wwwyo/dotfiles).
#
# model/effort inherit the org default in .github/pullfrog.org.config.sh
# (wwwyo/dotfiles). To override for this repo only, replace the pf_unset lines
# below with `pf_set model '<id>'` / `pf_set effort '<n>'`.
set -euo pipefail

REPO="wwwyo/andon"
PF=(mise exec -- pullfrog)

pf_set()   { "${PF[@]}" config set   "$1" "$2" --repo "$REPO" --yes; }
pf_unset() { "${PF[@]}" config unset "$1"     --repo "$REPO" --yes; }


pf_set enabled 'true'
pf_unset model   # inherit org default
pf_unset effort  # inherit org default
pf_set progress-comments 'true'
pf_set oss 'true'
pf_set push 'enabled'
pf_set shell 'restricted'
pf_set signed-commits 'false'
pf_set auto-merge 'false'
pf_set mention.enabled 'true'
pf_set mention.non-collaborators 'false'
pf_set review.mode 'agent'
pf_set review.non-collaborators 'false'
pf_set review.re-review 'false'
pf_set review.approve 'false'
pf_set review.drafts 'true'
pf_set review.own-prs 'false'
pf_set review.status-check 'true'
pf_set review.approval-check 'true'
pf_set issue.mode 'none'
pf_set issue.non-collaborators 'true'
pf_set label.enabled 'false'
pf_set address-reviews.enabled 'true'
pf_set fix-ci.own-prs 'true'
pf_set fix-ci.reviewed-prs 'false'

"${PF[@]}" config set hooks.setup --repo "$REPO" --yes --file - <<'PULLFROG_HOOK_SETUP'
# mise toolchain: install mise if absent, install repo tools, expose shims on PATH
# NB: set -e is intentionally AFTER the file guard — `ls` exits non-zero when
# only some of the files exist, and pipefail would turn that into a false negative.
ls mise.toml .mise.toml .config/mise.toml 2>/dev/null | grep -q . || exit 0
set -euo pipefail
command -v mise >/dev/null 2>&1 || curl -fsSL https://mise.run | sh
export PATH="$HOME/.local/bin:$PATH"
mise trust -a 2>/dev/null || true
mise install -y
mkdir -p "$HOME/.local/bin"
ln -sf "$HOME"/.local/share/mise/shims/* "$HOME"/.local/bin/ 2>/dev/null || true
PULLFROG_HOOK_SETUP


# explicit unsets — keep the backend converged on this file
# `instructions` stays unset so the org default applies (see pullfrog.org.config.sh)
pf_unset instructions
pf_unset env-allowlist
pf_unset hooks.post-checkout
pf_unset hooks.pre-push
pf_unset hooks.stop
pf_unset prompts.review
pf_unset prompts.build
pf_unset prompts.plan
pf_unset prompts.address-reviews
pf_unset prompts.fix-ci
pf_unset mention.instructions
pf_unset issue.instructions
pf_unset label.instructions

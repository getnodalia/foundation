# Agent instructions (`AGENTS.md`)

Every Nodalia repository has one `AGENTS.md`, written and maintained by Nodalia. `CLAUDE.md`, if
present, contains only `@AGENTS.md` on its first line (plus, at most, a note that AGENTS.md is
the file to edit). `agents-check.yml` checks both.

The file is for agents **and** human developers: it says what the app is and how to change it
safely, in the fewest words that are still exact. General rules live here in `foundation`; an
`AGENTS.md` links to them and adds only what is particular to its repository.

## Required sections

Use these headings (the check matches them case-insensitively):

1. **What this is**: the app, its users, platforms and editions, licence, app ID.
2. **Architecture**: crates/modules and what each is responsible for, the dependency direction,
   where a new feature of each kind goes.
3. **Build and test**: exact commands for the gate, the fast loop, running the app, and tests
   that need extra inputs (fonts, corpora, GPU) and how they skip without them.
4. **Rules**: the repository's hard rules (crash safety, clean room, assets, layering, never block
   the UI thread...), each with what enforces it.
5. **NDL**: how this app uses the Nodalia Design Language (which `nodalia-design` package, pinned
   how) and what is still missing. Nodalix OS documents its GNOME/Adwaita exception here.
6. **Release**: how a release is cut for this app, which artifacts, and what a maintainer does.
7. **Pull requests**: acceptance criteria for a change in this repository.

Optional: "Known traps", "Upstream" (for inherited code: the mirror branch and rename tool).

## Rules every agent follows (do not repeat them in each repo)

- Read the code you change and its tests before changing it. Confirm a cause in the code.
- Fix the problem where it is; add a test that fails without the fix.
- No dead code, no mocks that hide real failures, no empty abstractions, no TODO placeholders that
  pretend to work, no mass changes without tests.
- Never weaken a check, skip a test or add `continue-on-error` to get green.
- Report only what ran. Say what could not be run.
- One topic per PR, small enough to review. The PR title and first sentence make sense to someone
  who never saw the conversation.
- Merge your own PR once its required checks pass and reviews are resolved; fix non-required
  failures afterwards.
- Never push tags, publish releases, change billing, add paid services, or touch signing secrets
  without the maintainer's explicit go-ahead.
- Code, comments and commits in English; conventional commits where the repository uses them.
- Do not say in a PR that an agent wrote it unless the repository asks for it.
- Never describe a Nodalia app as a fork in user-facing text; keep legal notices intact.

## Template

`templates/AGENTS.md`.

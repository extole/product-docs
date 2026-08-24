@AGENTS.md
@.mintlify/AGENTS.md
@.claude/rules/product-docs-style.md

## Why this file exists alongside AGENTS.md

Claude Code reads `CLAUDE.md`. It does not read `AGENTS.md`, and it has no equivalent of Cursor's
glob-scoped auto-attach for rule files. Without this file a Claude Code session in this repo starts
with none of the repo's standards loaded.

## Why `.mintlify/AGENTS.md` is imported directly

That file holds the writing standards, and it is canonical because Mintlify's agent reads it and
cannot follow links (see `AGENTS.md`). The always-on rule only *points* at it, which is enough for
a tool that can chase a pointer -- but nearly every session in this repo is a docs edit, so lazy
loading buys little and risks the standards simply not being read. Importing it costs about 230
lines per session and makes the guarantee complete.

The import path ends in `.md`, so it resolves. Confirm it actually landed by asking the session to
"state the standards marker": the file's canary section defines the expected reply. The same trick
works on any other surface -- it is how to tell whether Mintlify's web editor loads the file on its
inline "Edit with AI" path, which is documented for agent sessions but unverified for selections.

## Why the rule imports point at `.claude/rules/`

An `@` import resolves a literal path ending in `.md`. It silently ignores a `.mdc` path, a glob
(`@.agents/rules/*.mdc`) and a directory (`@.agents/rules/`) -- all measured on CLI 2.1.228. Every
`@.agents/rules/<name>.mdc` line this file used to carry therefore imported nothing: a marker placed
inside a rule file was provably absent from a session's context.

So `.claude/rules/<name>.md` is a committed symlink to the real rule file, and the import points at
the symlink. Each rule keeps exactly one copy, nothing is renamed or moved, and Cursor's view of
`.agents/rules` is unchanged. `.claude/rules/` is an extension adapter for one tool, in the same
spirit as the existing `.claude/skills` symlink.

Adding a rule? Add the symlink and the `@` line, or Claude Code will not see it:

```bash
ln -s ../../.agents/rules/<name>.mdc .claude/rules/<name>.md
```

An import naming a file that no longer exists is skipped silently and does not break the imports
after it, so this file fails by quietly missing a rule rather than by erroring.

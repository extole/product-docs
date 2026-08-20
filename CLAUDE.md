@AGENTS.md
@.claude/rules/product-docs-style.md

## Why this file exists alongside AGENTS.md

Claude Code reads `CLAUDE.md`. It does not read `AGENTS.md`, and it has no equivalent of Cursor's
glob-scoped auto-attach for rule files. Without this file a Claude Code session in this repo starts
with none of the repo's standards loaded.

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

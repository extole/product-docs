@../AGENTS.md
@rules/product-docs-style.md

<!--
Maintainer notes. Block-level HTML comments are stripped before this file is injected
into Claude's context, so everything below costs zero startup tokens and stays readable
in the repo. Keep rationale here, not above the fold.

## Why this file exists alongside AGENTS.md

It lives at .claude/CLAUDE.md rather than the repo root -- both are documented project-
instruction locations, and .claude/ is a Mintlify built-in ignore, so nothing here can leak
onto docs.extole.com the way the root AGENTS.md once did. Imports resolve relative to this
file, hence @../AGENTS.md.

Claude Code reads `CLAUDE.md`; it does not read `AGENTS.md`. Without this file a Claude Code
session in this repo starts with none of the repo's standards loaded. Importing `AGENTS.md` from a
`CLAUDE.md` is what Anthropic documents for a repo that already has one.

Claude Code *does* have an equivalent of Cursor's glob-scoped auto-attach -- `paths:` frontmatter on
a file in `.claude/rules/`, which this file used to say did not exist. We deliberately do not use it
for the style rule: path-scoped rules trigger when Claude **reads** a matching file, and authoring a
new page writes one without ever reading it, so the standards would go unloaded in exactly the
workflow that needs them most.

The writing standards in `.mintlify/AGENTS.md` are therefore **not** imported here. They are ~230
lines against a documented target of under 200 per CLAUDE.md, and imports count against startup
context in full. The always-on rule below is 38 lines and instructs Claude to read that file, which
is enough for a tool that can follow a pointer -- unlike Mintlify's agent, which is why the file is
written flat in the first place.

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
-->

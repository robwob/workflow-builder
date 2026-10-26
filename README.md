# Workflow builder

A visual tool for designers to chain design skills into a named workflow with
approval gates, then export it.

## Use it

Open `workflow-builder.html` in a browser. It is a single self-contained file, with
no install and no server.

1. **Build.** Drag skill cards from the library onto the canvas and add steps:
   run a skill, wait for approval, ask a question, or do things together.
2. **Take it away.** Export the flow as a paste-into-the-app request, a `SKILL.md`
   file, or a prompt to paste into a chat. Codex is the default target, and the
   export wording also works for Claude Code.

Saved flows live in your browser's localStorage and are not uploaded anywhere.
"My skills" reads names and descriptions from a folder you pick, and nothing leaves
your machine. You can also paste any public GitHub repo address (or a folder or
`SKILL.md` inside one) under "Skills on GitHub". The page reads names and descriptions
only. Adding a skill does not install it: it must also be installed where the flow runs.

## Caveats

- A pause in an exported flow is an instruction to the model, not something the
  tool enforces.
- Export has not been tested on a real Codex install: that the app finds a skill
  saved to `~/.agents/skills`, that it will write there from a pasted request, and
  that a pause holds.
- The library lists design skills that you need installed separately. A flow that
  names a skill you do not have will not run that step.

GitHub limits unauthenticated requests to 60 an hour per network address. Each repo
added costs one of them.

## Rebuild

`template.html` is the source. `build.py` reads `~/.claude/skills/*/SKILL.md`,
merges the labels from `CURATED`, and writes `workflow-builder.html`:

    python3 build.py

#!/usr/bin/env python3
"""Scan installed skills and write workflow-builder.html (self-contained).

Run: python3 build.py
Skills are read from ~/.claude/skills/*/SKILL.md. Curated skills get
designer-friendly labels from CURATED below; anything else is listed
under "More skills" with its own description trimmed.
"""
import json
import re
from pathlib import Path

HERE = Path(__file__).parent
SKILLS_DIR = Path.home() / ".claude" / "skills"

# name -> (group, label, what you get, when to use it)
CURATED = {
    "brief": ("Start and plan", "Write a project brief",
              "A brief and a step-by-step plan for the project",
              "At the start, before any design"),
    "house-rules-setup": ("Start and plan", "Set up your house rules",
                          "A file of your own design preferences that the other skills follow",
                          "Once, so reviews match how you work"),
    "ux-research-brief": ("Research", "Plan user research",
                          "A research plan and the right methods for your question",
                          "When you need to find out something about users"),
    "desk-research": ("Research", "Research competitors",
                      "A summary of what competitors do, written as ideas to test",
                      "Before designing, to see the landscape"),
    "discussion-guide": ("Research", "Write interview questions",
                         "A script for user interviews",
                         "After you have a research plan"),
    "usability-test-plan": ("Research", "Plan a usability test",
                            "Tasks and a plan for testing with real users",
                            "When you have something to put in front of people"),
    "survey-questions": ("Research", "Write or check a survey",
                         "Survey questions, or a bias check of yours",
                         "When you need numbers, not stories"),
    "card-sort-analysis": ("Research", "Analyse a card sort",
                           "What your card sort results do and do not show",
                           "After a card sort has run"),
    "analyse-themes": ("Strategy", "Find the design strategy",
                       "A report on the strategic approach a page takes",
                       "When you want to understand why a design works"),
    "define-levers": ("Strategy", "Choose what to change",
                      "The levers worth moving, and the psychology behind them",
                      "After themes, before redesigning"),
    "discovery": ("Design", "Explore the layout",
                  "A greyscale wireframe that explores structure",
                  "First design step, before any styling"),
    "interaction": ("Design", "Map every state",
                    "Wireframes of states and interactions: error, empty, loading",
                    "After the layout is approved"),
    "ui": ("Design", "Style the design",
           "A fully styled design with real copy",
           "After the interactions are approved"),
    "design-review": ("Review", "Full design review",
                      "One prioritised report across flow, visuals and words",
                      "When you want everything checked at once"),
    "ux-review": ("Review", "Check the flow",
                  "Usability problems in the journey, ranked by severity",
                  "To find where people will get stuck"),
    "ui-review": ("Review", "Check the visuals",
                  "Contrast, type, spacing and hierarchy problems, ranked",
                  "To find why something looks off"),
    "content-review": ("Review", "Check the words",
                       "Copy problems in labels, errors and headings, ranked",
                       "To check that the text is clear"),
}

GROUP_ORDER = ["Start and plan", "Research", "Strategy", "Design", "Review"]


def frontmatter(text):
    m = re.match(r"^---\n(.*?)\n---", text, re.S)
    if not m:
        return {}
    out, key = {}, None
    for line in m.group(1).split("\n"):
        kv = re.match(r"^([A-Za-z_-]+):\s*(.*)$", line)
        if kv:
            key, val = kv.group(1), kv.group(2).strip()
            if val in (">", "|", ">-", "|-"):
                val = ""
            out[key] = val.strip("'\"")
        elif key and line.startswith((" ", "\t")):
            out[key] = (out[key] + " " + line.strip()).strip()
    return out


def first_sentence(s, limit=110):
    s = re.split(r"(?<=[.!?])\s", s.strip())[0]
    return s if len(s) <= limit else s[: limit - 1].rstrip() + "..."


def scan():
    found = {}
    for d in sorted(SKILLS_DIR.iterdir()):
        sk = d / "SKILL.md"
        if not sk.exists():
            continue
        fm = frontmatter(sk.read_text(errors="replace"))
        found[d.name] = fm
    return found


def main():
    found = scan()
    skills = []
    for name, (group, label, gives, when) in CURATED.items():
        skills.append({
            "name": name, "group": group, "label": label, "gives": gives,
            "when": when, "installed": name in found,
            "blocked": found.get(name, {}).get("disable-model-invocation") == "true",
        })
    # Only the curated set is shared. Anything else on this machine is personal,
    # and each designer adds their own through the page's folder picker.
    skills.sort(key=lambda s: GROUP_ORDER.index(s["group"]))
    html = (HERE / "template.html").read_text()
    html = html.replace("/*SKILLS_JSON*/[]", json.dumps(skills, indent=1))
    out = HERE / "workflow-builder.html"
    out.write_text(html)
    missing = [s["name"] for s in skills if not s["installed"]]
    print(f"{len(skills)} skills written to {out}")
    if missing:
        print("Not installed (shown as warnings in the page):", ", ".join(missing))


if __name__ == "__main__":
    main()

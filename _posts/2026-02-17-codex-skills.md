---
layout: post
title: "Codex Skills: Baking Your Workflow Into the Tool"
read_time: 2
---

*A follow-up to [I Fell in Love with Coding Again]({% post_url 2026-02-13-i-fell-in-love-with-coding-again %})*

In that post I shared a simple workflow: know the system and ask precise questions, break tasks into steps, and use automation for the boring parts. What I didn't mention is how often I was *repeating* those same instructions. Once that pattern was clear, I started encoding it—that's when **Skills** in Codex became a big part of my day.

Before diving in, it helps to be clear on the difference between the **agent** and a **skill**, and when to use which.

---

## Agent vs. Skill: When to Use What

| | **Agent (Codex)** | **Skill** |
|---|-------------------|-----------|
| **What it is** | The general-purpose AI. You give it intent and context; it plans, reads code, edits, runs commands. | A packaged playbook: instructions, templates, optional scripts. One focused workflow. |
| **Use when** | Open-ended work: "explain this codebase," "implement this feature," "fix this bug," "refactor X." | You do the *same* workflow over and over and want it consistent and one-tap. |
| **Where it lives** | Codex itself (CLI, IDE, app). | A folder with `SKILL.md` (and optionally scripts/references). You or your team create or install skills. |

**Rule of thumb:** If you find yourself pasting the same block of instructions or saying "like last time, but for X," that's a candidate for a skill. The agent does the work; the skill tells it *how* to do that kind of work every time.

---

## What I Actually Use Skills For

Most of my skills are **local, day-to-day**—things that used to be manual or a wall of prompts. Two big buckets:

### 1. Jira: From a few details to a real ticket

I give Codex a short description and maybe a doc link. The skill:

- Uses a **ticket description template** I keep in the skill (in `references/` or in the instructions).
- Sets the **fields** we care about: type, priority, board, assignee, labels, etc.
- Creates the ticket and attaches it to the right board, assigned to the right team.

**Before:** Copy template, fill fields, attach, assign. **After:** "Create a Jira ticket for &lt;brief description&gt;" and the skill does the rest. Huge reduction in busywork.

### 2. Git: Housekeeping as a single flow

Our housekeeping is a chain of small steps. I turned them into **small skills** and then **one combined skill** that runs the full flow:

| Step | What the skill does |
|------|----------------------|
| New branch | Create branch from the right base (e.g. `main`) with our naming convention. |
| Update from origin | Stash current changes → pull from `origin/main` → re-apply stash → handle conflicts if needed. |
| Commit | Generate commit message from **my template** (what changed, why, scope). |
| Push | Push branch and set upstream if needed. |

I can still run the small skills individually (e.g. "just create a commit message"), but the combined skill is what I use most: one prompt, full flow. That's the pattern—**small skills you can mix or run as one**.

### 3. Next: Codebase-specific skills

I'm now turning **recurring codebase prompts** into skills: "how we add a new API route," "how we update the schema and migrations," "how we add a component to the design system." Same idea—capture the steps and templates once, then invoke with a short prompt. That's the direction I want to expand: more repo-specific skills so my usual prompts become reliable, repeatable workflows.

---

## How Skills Work (Without Slowing You Down)

Skills use **progressive disclosure**:

- **Startup:** Codex loads only skill *names* and *descriptions*.
- **On demand:** When you use a skill, it loads the full `SKILL.md`.

So you can have many skills; they don't bloat context until invoked. Keeps the CLI fast and the session clean.

---

## Where Skills Live

| Scope | Location | Good for |
|-------|----------|----------|
| **Repo** | e.g. `.codex/skills/` or `.agents/skills/` | Team conventions: Jira template, code review, "how we add a feature." |
| **User** | Your config (e.g. `~/.codex/skills/` or `~/.agents/skills/`) | Personal workflows: Git flow, commit template, prompt-optimization. |
| **System** | Bundled with Codex | Built-ins (e.g. skill-creator). |

I keep **Jira and Git** in my user skills (same flow across projects). **Codebase-specific** ones live in the repo so the team shares them.

---

## How to Arrange SKILL.md: A Proper Format

Codex only *requires* a `SKILL.md` with **frontmatter** (`name`, `description`) and a body. How you arrange the body is up to you—but a consistent structure makes skills easier to write, read, and refine. Here's a format I use and that you can adapt.

### Required: Frontmatter

```yaml
---
name: skill-name
description: One clear sentence: what this skill does and when Codex should use it.
---
```

- **name:** Lowercase, hyphens OK (e.g. `jira-ticket`, `git-housekeeping`). Codex uses this for `$skill-name`.
- **description:** This is what Codex uses to *match* your prompt. Be specific so the right skill triggers (or so you can pick it from the list).

### Body: Section layout that works

After the frontmatter, structure the rest of the file so the agent knows what to do and when. A good default arrangement:

| Section | Purpose |
|--------|---------|
| **Goal** | One short paragraph: what this skill achieves. |
| **Inputs** | What you (or the user) provide: e.g. brief description, doc link, branch name. |
| **Outputs** | What must be true when done: e.g. ticket on board and assigned, branch pushed. |
| **Workflow** (or **Steps**) | Numbered, imperative steps the agent follows. |
| **Template** (optional) | If the skill uses a fixed format (Jira body, commit message), put the template here or in `references/` and reference it in the steps. |
| **Example triggers** (optional) | Example phrases that should invoke this skill (helps implicit matching). |
| **Constraints** (optional) | What *not* to do, or rules (e.g. "Never assume assignee; always ask if missing"). |

You don't need every section for every skill—use what fits. For a tiny skill, Goal + Steps might be enough. For Jira, you'd add Inputs, Outputs, Template, and maybe Constraints.

### Full SKILL.md template

```markdown
---
name: my-skill-name
description: [What it does and when to use it. Codex uses this to select the skill.]
---

# My Skill Name

## Goal
[One short paragraph: what this skill achieves.]

## Inputs
- [What the user or context must provide, e.g. brief description, link, branch name.]

## Outputs
- [What must be true when the skill is done.]

## Workflow
1. [First imperative step.]
2. [Second step.]
3. [Continue until done.]

## Template
[Paste the template here, or: "Use the template in references/ticket-template.md and fill …"]

## Example triggers
- "Create a Jira for …"
- "File a ticket for …"

## Constraints
- [Any rules or things to avoid.]
```

### Defining your own format

You can change the section names and order to match how you think. For example:

- **Repo-specific:** Add a **Context** section ("This repo uses …") or **Key fields** ("Always set: type, priority, board, assignee").
- **Multi-step skills:** Add **Prerequisites** ("Run only when on a feature branch") or **Sub-skills** ("This skill calls the commit-message skill then the push skill").
- **Strict templates:** Put long templates in `references/` or `assets/` and keep SKILL.md to Goal, Steps, and "Use template at …".

The important part is: **arrange SKILL.md so the agent has a clear path**—goal, what it gets, what it must produce, and the steps in between. Once you pick a layout you like, reuse it so every skill feels familiar and easy to iterate on.

---

## Quick Examples (Less Wall of Text)

**Jira skill (conceptual)**  
- Input: short description + optional doc link.  
- Steps: fill ticket template, set type/priority/board/assignee/labels, create and attach.  
- Template and key fields live in the skill (references or SKILL.md).

**Git – small skills**  
- "Create branch from main with naming convention."  
- "Update my branch from origin/main (stash, pull, re-apply, resolve conflicts)."  
- "Generate commit message from template."  
- "Push and set upstream."

**Git – combined skill**  
- Runs the four steps in order; I trigger once and get the full housekeeping flow.

**Codebase-specific (target state)**  
- "Add a new API route" → skill knows our routing pattern, where to put files, how we register.  
- "Add a design-system component" → skill knows structure, exports, and story pattern.

---

## Using Skills in Codex

- **Explicit:** Type `$` in the CLI (or use `/skills` where available), pick the skill, then give your prompt.
- **Implicit:** If the skill's description and example triggers match your prompt, Codex can invoke it automatically.
- **Install more:** Use `$skill-installer` (or equivalent) to add skills from catalogs or GitHub so you're not starting from zero.

---

## Take the Long View (And Your Coffee)

Useful skills don't have to be perfect on day one. I've had the best results by:

- Starting with one painful, repetitive task (for me: Jira and Git).
- Turning it into a first version of a skill.
- Using it in real work, noting what's wrong or missing.
- Refining the steps and templates over a few sessions—often while having a coffee.

So: **agent** for open-ended work, **skill** for repeatable workflows. Start with day-to-day pain (tickets, git, one codebase task), use a simple framework to create and refine skills, and let them improve over multiple iterations. That's how skills have become one of the most useful parts of my setup—and how you can make them yours too.

---

*Further reading: [Codex Agent Skills](https://developers.openai.com/codex/skills), [Codex CLI features](https://developers.openai.com/codex/cli/features), [Slash commands](https://developers.openai.com/codex/guides/slash-commands/), [OpenAI skills on GitHub](https://github.com/openai/skills), and community resources like the [Codex Skills Catalog](https://jmerta.github.io/codex-skills/) and the [Habr deep dive on Codex Skills](https://habr.com/en/articles/984916/).*

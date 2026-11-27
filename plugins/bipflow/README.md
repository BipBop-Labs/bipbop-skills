# bipflow

Git workflow skills for coding agents: commit and open pull requests the way
a careful teammate would.

| Skill | Invoke as | Purpose |
| --- | --- | --- |
| `commit` | `/bipflow:commit` | Create atomic, well-written commits: review the real diff, stage files explicitly, follow the repository style, and obey the hooks. |
| `pr` | `/bipflow:pr` | Open a pull request with a technical summary, a test plan, and a client summary in Spanish. The pull request targets `stg` when the repository has one. If not, it targets the default branch. On `stg`, the skill tells a new work branch apart from a promotion to the default branch. |

## Install

```text
/plugin marketplace add BipBop-Labs/bipbop-skills
/plugin install bipflow@bipbop
```

Codex CLI:

```bash
codex plugin marketplace add BipBop-Labs/bipbop-skills --ref main
codex plugin add bipflow@bipbop
```

## Update

```text
/plugin marketplace update bipbop
/plugin update bipflow@bipbop
/reload-plugins
```

Codex CLI:

```bash
codex plugin marketplace upgrade bipbop
```

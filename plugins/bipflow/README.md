# bipflow

Git workflow skills for coding agents: commit and open pull requests the way
a careful teammate would.

| Skill | Invoke as | Purpose |
| --- | --- | --- |
| `commit` | `/bipflow:commit` | Create atomic, well-written commits: review the real diff, stage explicitly, follow the repository style, respect hooks. |
| `pr` | `/bipflow:pr` | Open a pull request with a technical summary, a test plan, and a client-facing summary in Spanish. |

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

# Enforcement options by stack

Use this table when an accepted ADR can be turned into a check. Pick the tool
the repository already runs when possible. Verified 2026-10-02.

| Stack | Tool | What it checks | Runs as |
| --- | --- | --- | --- |
| Java / Kotlin | [ArchUnit](https://github.com/TNG/ArchUnit) | package and class dependencies, layering, naming, cycles | JUnit test |
| Kotlin | [Konsist](https://github.com/LemonAppDev/konsist) | structure and architecture rules | unit test |
| JS / TS | [dependency-cruiser](https://github.com/sverweij/dependency-cruiser) | forbidden imports, cycles, orphans | CLI |
| JS / TS | [eslint-plugin-boundaries](https://github.com/javierbrea/eslint-plugin-boundaries) | allowed imports between element types | ESLint |
| JS / TS | [eslint-plugin-import `no-restricted-paths`](https://github.com/import-js/eslint-plugin-import) | imports from forbidden zones | ESLint |
| JS / TS (Nx) | `@nx/enforce-module-boundaries` | tag-based project boundaries | ESLint |
| Python | [import-linter](https://github.com/seddonym/import-linter) | layer, forbidden and independence contracts | CLI `lint-imports` |
| Python | [tach](https://github.com/gauge-sh/tach) | module boundaries and public interfaces | CLI |
| Go | [go-arch-lint](https://github.com/fe3dback/go-arch-lint) | component import allow-lists | CLI |
| Go | [depguard](https://github.com/OpenPeeDeeP/depguard) | allowed and denied packages | golangci-lint |
| .NET | [ArchUnitNET](https://github.com/TNG/ArchUnitNET) | dependency and naming rules | unit test |
| Rust | [cargo-deny](https://github.com/EmbarkStudios/cargo-deny) | banned crates, licenses, sources (external deps only) | CLI |
| PHP | [deptrac](https://github.com/deptrac/deptrac) | layer dependency rules | CLI |
| PHP | [phparkitect](https://github.com/phparkitect/arkitect) | namespace, dependency, naming rules | CLI |
| Ruby | [packwerk](https://github.com/Shopify/packwerk) | package privacy and dependencies | CLI |
| Any language | [semgrep](https://github.com/semgrep/semgrep) | custom pattern rules | CLI / CI |
| Any language | [Danger](https://github.com/danger/danger) | PR rules (changed files, missing ADR) | CI on PRs |
| Any language | grep in CI, [pre-commit](https://github.com/pre-commit/pre-commit) | forbidden strings or imports | shell step / git hook |
| Config files | [conftest](https://github.com/open-policy-agent/conftest) | Rego policies over YAML, JSON, HCL, Dockerfile | CLI / CI |

## Deciding enforceable vs advisory

Enforceable when the decision reduces to one of:

- "module A must not import module B" (dependency rule);
- "only X may be used for Y" (banned alternatives: a dependency, an API, a string);
- "every file matching P must contain or not contain Q" (pattern rule);
- "config key K must equal V" (config rule).

Advisory when the decision is about process, taste, or trade-offs that need
judgement ("prefer small PRs", "keep the domain layer thin"). Record it, tag the
code with `@decision`, and rely on `/adr:review`.

Caveats: NetArchTest has had no commits since mid-2024, prefer ArchUnitNET.
cargo-deny governs external crates, not internal layering. pytest-archon is
small and low-activity.

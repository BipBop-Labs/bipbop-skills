# Sources and strength of evidence

Read this when someone asks where a recommendation in this skill comes from, how far to trust it, or where the sources disagree, and to find a vendor's own guidance for a specific model.

Compiled in October 2026. The skill is a synthesis in our own words; nothing here is copied from the sources at length.

## How to read the evidence

Three kinds of source stand behind the skill, and they deserve different weight.

- **Independent studies** (peer-reviewed papers and preprints with a stated method). These are the strongest, with two limits: nearly all were run on models from 2024 and 2025, and most measure multiple-choice accuracy or simple checkable constraints, which is far from what an agent's system prompt has to do.
- **Vendor guidance** (documentation and engineering posts from Anthropic and OpenAI). It reflects wide experience with current models, but the numbers in it are the vendors' own internal results, and each vendor has reversed its own advice between model generations.
- **Practitioner synthesis.** One third-party repository contributed framing; its claims are mostly unsourced opinion.

When a recommendation matters for a decision, test it on the model in question. That is the only evidence that is both current and specific.

## Evidence behind each recommendation

| Recommendation in the skill | Independent evidence | Vendor guidance |
| --- | --- | --- |
| Include only the context the task needs | Strong: accuracy falls with input length and with distractors (Levy 2024, NoLiMa 2025, Chroma 2025) | Agrees |
| Fewer instructions are followed better; put the important ones first | Strong (IFScale 2025; Harada 2025) | Agrees |
| Remove contradictions; a stated priority order is not enough | Strong: system-versus-user conflicts are resolved unreliably (IHEval 2025; Geng 2026) | Agrees that conflicts are costly |
| Give the whole task in one place | One large preprint (Laban 2025) | Agrees |
| Step-by-step prompting helps non-reasoning models on maths and logic, and adds little on reasoning models | Strong (Sprague 2025; Wharton Report 2) | Agrees |
| Put working before the answer; separate reasoning from formatting | Strong across four studies (Tam 2024; Format Tax 2026 and others) | Agrees |
| Strict output formats can cost quality on small models | Mixed: real on small and open models, mostly gone on recent large ones | Recommends schema features |
| Self-review without an outside signal rarely helps | Strong (Stechly 2024; Kamoi 2024; RefineBench 2026) | Mixed, and varies by model |
| A role line does not improve accuracy | Strong (Zheng 2024; Wharton Report 4) | Recommends roles for tone and focus |
| Tips, threats and emotional appeals do nothing reliable | Strong; the best-replicated null result (Wharton Reports 1 and 3; Vaugrante 2024) | Agrees |
| Wording and format changes move results, less on large models | Strong (Sclar 2024; Seleznyov 2025) | Agrees |
| Clear statements of purpose in tool descriptions improve tool selection | Moderate: three recent studies, mostly preprints | Agrees |
| Too many tools degrade selection | Mixed; published thresholds come from weak studies | Agrees; suggests roughly 20 as a soft limit |
| Explain the reason behind a rule | None found | Both vendors recommend it |
| Positive instructions work better than prohibitions | Weak: old negation studies and one unreplicated preprint; no direct comparison | Both vendors recommend it |
| Capitals and emphatic words cause over-application | None found on compliance | Both vendors report it |
| Describe outcomes instead of scripting steps | None found | Both vendors recommend it for current large models |
| Examples are imitated closely and can narrow behaviour | None found directly; older work shows examples mainly convey format | Vendors report it for current models |
| Long documents before the question | Not confirmed on recent models; the supporting result is from 2023 | Anthropic reports an internal gain |
| A specific delimiter (XML, Markdown, plain text) is best | None found; no format wins consistently | Examples vary; consistency is the common ground |

## Where the sources disagree

The skill takes a position on each of these; the reasoning is given so it can be revisited.

- **Examples.** Earlier vendor guidance treated examples as the most reliable steering tool. Guidance from mid-2026 says they constrain current models, and OpenAI says they can hurt reasoning models. The skill keeps examples for formats and voice that description cannot pin down, and asks for a test with and without.
- **Length of tool descriptions.** Anthropic's platform documentation asks for detailed descriptions of several sentences; its later engineering writing reports replacing a very long description with one sentence and a well-designed schema. The skill's rule is to state what the model could not guess, and to let the schema carry what it can.
- **Where tool guidance lives.** One vendor's function-calling guide puts when-to-use guidance in the system prompt; later guidance from both vendors puts it in the tool description. The skill puts tool-specific guidance in the description and cross-tool policy in the system prompt.
- **Self-verification reminders.** They help some models and cause wasted work on others, within the same vendor's documentation. The skill asks for outside checks and treats reminders as a fix for an observed problem.
- **Strong wording.** Some engineering posts report that an emphatic instruction was needed to stop a specific failure; guidance elsewhere warns against emphasis. The skill allows emphasis on one line for one observed failure.
- **Stating the reason.** Most guidance favours giving the reason; one page on skill files favours stating only what to do, to save tokens. The skill asks for a clause, not a paragraph.
- **Initiative, verbosity, formatting, delegation.** Every vendor's defaults have flipped between generations. The skill treats them as settings to state explicitly.

## Vendor guidance

Start from these pages when the target model is known. Each vendor publishes a page per model, organised as "if you observe this, change that"; read the one for the model in use, since those pages contradict each other across models.

Anthropic:

- Prompting best practices, with links to the per-model pages: https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices
- Skill authoring best practices: https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices
- Define tools: https://platform.claude.com/docs/en/agents-and-tools/tool-use/define-tools
- Define success criteria and build evaluations: https://platform.claude.com/docs/en/test-and-evaluate/develop-tests
- Effective context engineering for AI agents (September 2025): https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
- Writing effective tools for agents (September 2025): https://www.anthropic.com/engineering/writing-tools-for-agents
- How we built our multi-agent research system (June 2025): https://www.anthropic.com/engineering/multi-agent-research-system
- Demystifying evals for AI agents (January 2026): https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents
- Harness design for long-running application development (March 2026): https://www.anthropic.com/engineering/harness-design-long-running-apps
- The new rules of context engineering for Claude 5 generation models (July 2026): https://claude.dev/blog/the-new-rules-of-context-engineering-for-claude-5-generation-models/

OpenAI:

- Prompt guidance for the current model, with links to earlier ones: https://developers.openai.com/api/docs/guides/prompt-guidance
- Function calling, including best practices for defining functions: https://developers.openai.com/api/docs/guides/function-calling
- Reasoning best practices: https://developers.openai.com/api/docs/guides/reasoning-best-practices
- Evaluation best practices: https://developers.openai.com/api/docs/guides/evaluation-best-practices
- Prompting guides for earlier models, useful for seeing what was later reversed: https://developers.openai.com/cookbook

Google's prompting guidance was reviewed and left out. Its prompt-design pages were written for earlier models and had not been revalidated for the current ones at the time of writing.

## Independent studies

- Levy, Jacoby, Goldberg. "Same Task, More Tokens." ACL 2024. https://arxiv.org/abs/2402.14848
- Modarressi et al. "NoLiMa: Long-Context Evaluation Beyond Literal Matching." ICML 2025. https://arxiv.org/abs/2502.05167
- Hong, Troynikov, Huber. "Context Rot." Chroma technical report, 2025 (not peer-reviewed; published by a retrieval vendor). https://www.trychroma.com/research/context-rot
- Liu et al. "Lost in the Middle." TACL 2023. https://arxiv.org/abs/2307.03172
- Laban et al. "LLMs Get Lost In Multi-Turn Conversation." Preprint, 2025. https://arxiv.org/abs/2505.06120
- Jaroslawicz et al. "How Many Instructions Can LLMs Follow at Once?" Preprint, 2025. https://arxiv.org/abs/2507.11538
- Harada et al. "When Instructions Multiply." Findings of EMNLP 2025. https://arxiv.org/abs/2509.21051
- Zhang et al. "IHEval: Evaluating Language Models on Following the Instruction Hierarchy." NAACL 2025. https://arxiv.org/abs/2502.08745
- Geng et al. "Control Illusion: The Failure of Instruction Hierarchies in Large Language Models." AAAI 2026. https://arxiv.org/abs/2502.15851
- Sprague et al. "To CoT or not to CoT?" ICLR 2025. https://arxiv.org/abs/2409.12183
- Meincke, Mollick, Mollick, Shapiro. Prompting Science Reports 1 to 3, Wharton Generative AI Labs, 2025 (not peer-reviewed). https://arxiv.org/abs/2503.04818, https://arxiv.org/abs/2506.07142, https://arxiv.org/abs/2508.00614
- Basil et al. "Prompting Science Report 4: Playing Pretend." 2025 (not peer-reviewed). https://arxiv.org/abs/2512.05858
- Zheng et al. "When 'A Helpful Assistant' Is Not Really Helpful." Findings of EMNLP 2024. https://arxiv.org/abs/2311.10054
- Vaugrante, Niepert, Hagendorff. "A Looming Replication Crisis in Evaluating Behavior in Language Models?" Preprint, 2024. https://arxiv.org/abs/2409.20303
- Sclar et al. "Quantifying Language Models' Sensitivity to Spurious Features in Prompt Design." ICLR 2024. https://arxiv.org/abs/2310.11324
- Seleznyov et al. "When Punctuation Matters." Findings of EMNLP 2025. https://arxiv.org/abs/2508.11383
- Tam et al. "Let Me Speak Freely?" EMNLP 2024 Industry Track. https://arxiv.org/abs/2408.02442
- Lee, D'Antoni, Berg-Kirkpatrick. "The Format Tax." Preprint, 2026. https://arxiv.org/abs/2604.03616
- Stechly, Valmeekam, Kambhampati. "On the Self-Verification Limitations of Large Language Models on Reasoning and Planning Tasks." ICLR 2025. https://arxiv.org/abs/2402.08115
- Kamoi et al. "When Can LLMs Actually Correct Their Own Mistakes?" TACL 2024. https://arxiv.org/abs/2406.01297
- Lee et al. "RefineBench." 2025. https://arxiv.org/abs/2511.22173
- Hasan et al. "Model Context Protocol (MCP) Tool Descriptions Are Smelly!" Preprint, 2026. https://arxiv.org/abs/2602.14878
- Schulhoff et al. "The Prompt Report." Preprint, 2024; a survey of techniques. https://arxiv.org/abs/2406.06608

## Practitioner synthesis

- Denis Shiryaev, `agents-best-practices` (MIT licence): https://github.com/DenisSergeevitch/agents-best-practices. The step of checking whether a failure is a prompt problem before editing the prompt, and the idea of a handoff as an operational briefing, draw on its framing. Its prompt templates were not used, since they follow a style current vendor guidance advises against.

# Self Check

Run this checklist before claiming the analysis is complete.

## Evidence

- [ ] Every major conclusion cites a concrete file, section, script, interface, or resource-design choice.
- [ ] Pain points are inferred from implementation details, not copied from `description`.
- [ ] Uncertain claims are marked with `推测：` and include the basis for the inference.

## Workflow

- [ ] Structure scanning appears before subjective analysis.
- [ ] Missing resource categories are explicitly skipped instead of invented.
- [ ] Mermaid sequence diagram includes user, Agent, `SKILL.md`, optional resources, and output.
- [ ] Flowchart is included when there are meaningful branches or loops.

## Output Quality

- [ ] The document follows `references/output-template.md`.
- [ ] The scoring table uses all 8 rubric dimensions.
- [ ] The analysis includes assumptions, uncertainty, and next actions.
- [ ] Improvement suggestions identify concrete files or resources to change.

## Product Judgment

- [ ] At least 3 unique design moves are attempted.
- [ ] If fewer than 3 are justified, the limitation is stated honestly.
- [ ] Each design move includes common approach, Skill approach, design insight, boundary, and evidence.

## Iteration Rule

If the output fails any checklist item:
1. Fix the analysis first.
2. If the failure reveals missing guidance, update the appropriate reference file.
3. If the same failure happens twice, add a new pitfall or example to `references/examples.md`.

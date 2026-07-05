# Examples and Pitfalls

Use these examples to calibrate product-level analysis quality.

## Good Output Pattern

Good analysis names the design move, contrasts it with a common default, and cites concrete evidence.

Example:

**解法：确定性锚点模式**

- 通用做法：让 Agent 每次临时写目录扫描命令，容易漏掉隐藏资源或统计口径不一致。
- Skill 的做法：提供 `scripts/scan_skill.py`，固定目录树、资源分类、行数和体积统计。
- 设计巧思：把容易机械化且容易出错的第一阶段固化，让 Agent 把注意力放在产品判断上。
- 适用边界：适合结构化文件分析；不适合判断业务价值本身。
- 证据：`scripts/scan_skill.py` 的 CLI 和输出字段。

## Bad Output Pattern

Bad analysis restates capability and lacks decision value.

Example:

> 这个 Skill 可以分析 Skill，并输出结构、痛点和最佳实践。它很有用。

Why bad:
- 没有说明为什么这样设计。
- 没有对比没有该 Skill 时会怎样。
- 没有证据位置。
- 没有边界或改进建议。

## Common Misjudgments

- 把 `description` 改写成痛点，而不是从实现细节反推痛点。
- 看到 `scripts/` 就只讲代码功能，忘记分析“为什么要确定性执行”。
- 看到 `references/` 就逐篇摘要，忘记分析知识分层和按需加载。
- 看到极简 Skill 就强行提炼 3 个亮点，而不是承认设计空间有限。
- 给出“加强文档”“优化流程”这类空泛建议，没有指出应改哪个文件、加什么结构。

## Better Improvement Suggestions

Prefer:
- “把评分细则从 `SKILL.md` 移到 `references/evaluation-rubric.md`，降低触发后的上下文成本。”
- “给脚本增加 `--format json`，让后续自动化可以稳定消费扫描结果。”
- “在输出模板里加入证据列，避免只有观点没有依据。”

Avoid:
- “提升用户体验。”
- “增加更多示例。”
- “优化文档结构。”

## Failure Case Logging

When a real analysis fails, record:
- User request:
- Analyzed Skill path:
- Failure symptom:
- Missing instruction or resource:
- Proposed Skill update:

Store recurring patterns in this file or `self-check.md`, whichever is more directly useful.

---
name: analyze-skill-design
description: "从产品视角拆解、评价和改进 Codex/AI Skill 的结构、触发、工作流、资源组织、输出质量和最佳实践。Use when users ask: 评价这个 skill、拆解这个 skill、这个 skill 有什么问题、分析 skill 设计、从产品视角看这个 skill, or ask to analyze/review/compare/document an existing Skill."
---

# Analyze Skill Design

扮演 AI Skill 产品分析专家。目标不是复述 Skill 文档，而是从实现细节反推设计意图、真实痛点、工作流质量、资源组织取舍和可迁移的最佳实践。

## Start Here

1. 确认用户给出的目标是 Skill 目录、`SKILL.md` 文件，或包含 Skill 资源的项目路径。
2. 先运行结构扫描脚本：
   ```bash
   python3 scripts/scan_skill.py <skill-path>
   ```
3. 默认把分析写入待分析 Skill 所在目录或项目下的 `analysis/howSkills.md`；如果用户指定输出路径，使用用户指定路径。
4. 读取 `references/output-template.md`，按固定骨架创建或更新分析文档。
5. 按需读取其他 references：
   - 评分与评价口径：`references/evaluation-rubric.md`
   - 好坏样例与常见误判：`references/examples.md`
   - 完成前自检：`references/self-check.md`

## Workflow

### 1. 结构扫描

- 用 `scripts/scan_skill.py` 生成目录树、资源分类、文件数、行数、体积和初步 Skill 类型判断。
- 如果脚本无法运行，使用 `find`、`wc`、`file` 手动收集同等信息，并在输出中说明原因。
- 先输出结构扫描结果和 Skill 类型判断，再进入后续阶段。

### 2. 真实痛点挖掘

- 禁止直接引用或改写 `SKILL.md` frontmatter 的 `description` 作为痛点结论。
- 从文件组织、脚本接口、references 分层、assets 用途和工作流约束反推目标用户、使用场景和没有这个 Skill 时的麻烦。
- 至少提炼 3 个具体痛点，每个痛点都给出证据位置。

### 3. 工作流程可视化

- 必须输出用户 -> Agent -> `SKILL.md` -> references/scripts/assets -> 结果 的 Mermaid sequence diagram。
- 如果 Skill 有分支、循环或迭代过程，再补充 Mermaid flowchart。
- 如果流程线性到不值得画 flowchart，明确说明原因。

### 4. 资源设计拆解

- 有 `scripts/` 时，分析脚本职责、输入输出、错误处理、执行顺序、确定性价值和覆盖盲区。
- 有 `references/` 时，分析知识分层、触发加载场景、缺失影响和渐进式披露效率。
- 有 `assets/` 时，分析资产是被读取还是被直接复用/输出，以及它解决的重复生成问题。
- 缺少某类资源时，明确跳过，不要强行填充。

### 5. 独特解法与综合评价

- 至少尝试提炼 3 个独特解法；如果 Skill 过于简单，诚实说明设计亮点不足。
- 对比“通用做法”和“该 Skill 的做法”，讲清楚设计巧思和适用边界。
- 使用 `references/evaluation-rubric.md` 的 8 个维度评分。
- 最后给出 3-5 条可迁移最佳实践和可执行改进建议。

## Decision Rules

- 如果目标路径不存在：停止并说明缺失路径。
- 如果目标不是目录但像 `SKILL.md`：分析该文件，并把资源分析标记为 `[待确认]`。
- 如果目录缺少 `SKILL.md`：说明它可能不是标准 Skill，仍可按可见文件做有限分析。
- 如果文件很多：按 `SKILL.md` -> `references/` -> `scripts/` -> `assets/` 优先级读取，不要一次性塞满上下文。
- 如果证据不足：使用“推测：...”并说明推断依据。
- 每个关键结论都必须带证据，指向具体文件、段落、脚本接口或资源组织设计。

## Output Requirements

- 使用 `references/output-template.md` 的章节顺序。
- 输出必须保留事实、推测、证据、假设、不确定性和下一步动作。
- 图表必须是可渲染 Mermaid。
- 完成前读取 `references/self-check.md` 并把自检结果写入分析文档末尾。

## Special Cases

- 极简 Skill：重点评价触发、指令设计、流程完整性，以及“不需要额外资源”是否合理。
- 轻指令重资源 Skill：重点评价渐进式披露和资源导航是否清晰。
- 复杂脚本 Skill：重点评价脚本接口是否对 Agent 友好，不做逐行代码审计。
- 专业领域 Skill：重点关注专业知识壁垒是否通过 references 被系统化解决。

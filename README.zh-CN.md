# ADAC Skills

语言：[English](README.md) | **中文**

**ADAC** 是 **Acceptance-Driven Agentic Coding** 的缩写，可以翻译为“验收驱动的智能体协作开发”。它是一套面向 AI 辅助软件工程的正式交付机制：不要直接让 AI 大面积写代码，而是先定义上下文、边界、验收证据和人工关口，再扩大实现范围。

> 搜索关键词：**Acceptance-Driven Agentic Coding** 是 ADAC Skills 背后的完整方法名。

这个仓库包含 ADAC 的正式规范、可复用模板、portable agent skill、校验脚本和展示页面。它面向 Claude、Codex，以及其他能够消费 `SKILL.md` 风格指令的 AI Coding Agent。

> 说明：分发给 AI 使用的 `skills/adac/SKILL.md` 目前保持英文单份，避免同一套 agent 指令维护两份。中文内容主要服务于人类读者、介绍页和团队传播。

## 品牌定位

- **品牌名**：ADAC Skills
- **完整名称**：Acceptance-Driven Agentic Coding
- **Skill 名称**：`adac`
- **标语**：Acceptance first. Agents second.
- **核心承诺**：让 AI Coding 工作变得可审查、有证据、能进入上线判断。

## 机制概览

ADAC 由四个控制点组成：

1. **Context**：在写代码前，让 Agent 先拿到系统、业务规则、历史问题和已知风险。
2. **Spec**：在实现前写清目标行为、非目标、接口边界和回退路径。
3. **Evals**：把真实风险转成可执行的验收检查，包括行为、回归、性能、生命周期和可观测性。
4. **Gates**：架构、并发、安全、发布和残余风险判断由人来收口。

它不是简单的 TDD，也不是“提示词写得更详细”。ADAC 的目标是让 AI 产出不只停在“代码能编译”，而是能带着验收证据进入 review 和上线判断。

## 安装

通过 portable skills CLI 安装：

```bash
npx skills add HaloForgeAI/adac-skills --skill adac
```

安装后可以在支持 skills 的 Agent 中使用 `adac`，例如要求它在动手实现前先给出风险分级、上下文包、验收矩阵和人工关口。

## 使用方式

推荐提示词：

```text
Use ADAC for this task. Before editing code, classify risk, build a context pack from the repo, and propose an acceptance matrix with human gates.
```

中文表达也可以：

```text
用 ADAC 处理这个任务。先不要改代码，先做风险分级、上下文梳理、验收矩阵和人工关口设计。
```

## 验证 ADAC Plan

仓库内置了一个轻量校验脚本：

```bash
python3 scripts/validate_adac_plan.py examples/worker-module.adac.md
```

如果从 npm 安装，也可以使用：

```bash
npx adac-skills validate examples/worker-module.adac.md
```

## 示例场景

更完整的示例见 [docs/examples.md](docs/examples.md)，包括：

- 异步资源加载路径改造；
- 支付/优惠券流程变更；
- 管理后台批量操作；
- AI 生成测试计划的验收审查；
- 把一次性事故处理流程沉淀成团队 skill。

## 发布与分发

ADAC Skills 已经准备了多种分发形态：

- GitHub 仓库：`HaloForgeAI/adac-skills`
- npm 包：`adac-skills`
- Claude Code plugin manifest：`.claude-plugin/plugin.json`
- Claude Code marketplace catalog：`.claude-plugin/marketplace.json`
- Codex plugin manifest：`.codex-plugin/plugin.json`
- Portable skill：`skills/adac/`

更多发布说明见：

- [docs/distribution.md](docs/distribution.md)
- [docs/publishing-checklist.md](docs/publishing-checklist.md)
- [docs/brand.md](docs/brand.md)

## GitHub Pages

静态展示页位于 [docs/index.html](docs/index.html)，GitHub Pages 使用 `main` 分支的 `/docs` 目录发布。

当前页面地址：

<https://haloforgeai.github.io/adac-skills/>

## License

Apache-2.0

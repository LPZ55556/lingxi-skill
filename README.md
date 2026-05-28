# 灵犀 — 个性化情感陪伴 AI Skill

> *"把在意的人装进口袋。"*

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://python.org)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Skill-blueviolet)](https://claude.ai/code)
[![AgentSkills](https://img.shields.io/badge/AgentSkills-Standard-green)](https://agentskills.io)

&nbsp;

提供一个人的原材料（聊天记录、照片、朋友圈）加上你的主观描述
生成一个**真正像 ta 的 AI 陪伴者**
用 ta 的口头禅说话，用 ta 的方式回复你，记得你们一起经历过的事

支持克隆：朋友 · 恋人 · 家人 · 同事 · 师长 · 任何你在乎的人

[安装](#安装) · [使用](#使用) · [效果示例](#效果示例) · [English](README_EN.md)

---

## 安装

### Claude Code

> **重要**：Claude Code 从 **git 仓库根目录** 的 `.claude/skills/` 查找 skill。请在正确的位置执行。

```bash
# 安装到当前项目（在 git 仓库根目录执行）
mkdir -p .claude/skills
git clone https://github.com/LPZ55556/lingxi-skill .claude/skills/create-lingxi

# 或安装到全局（所有项目都能用）
git clone https://github.com/LPZ55556/lingxi-skill ~/.claude/skills/create-lingxi
```

### 依赖（可选）

```bash
pip3 install -r requirements.txt
```

---

## 环境要求

- **Claude Code**：免费安装，需要 Node.js 18+（[安装指南](https://docs.anthropic.com/en/docs/claude-code)）
- **API 消耗**：创建一个灵犀 Skill 大约消耗 5k-15k tokens，取决于聊天记录量
- **付费方式**（二选一）：
  - Claude Pro / Max 订阅：在订阅额度内使用，无需额外配置
  - Anthropic API Key：按量付费，需在 Claude Code 中配置 key
- **不需要 GPU**，不需要本地模型，不需要 Docker

---

## 使用

在 Claude Code 中输入：

```
/create-lingxi
```

按提示输入 ta 的代号、关系类型、性格画像，然后选择数据来源。所有字段均可跳过，仅凭描述也能生成。

完成后用 `/{slug}` 调用该灵犀 Skill，开始对话。

### 管理命令

| 命令 | 说明 |
|------|------|
| `/list-lingxi` | 列出所有灵犀 Skill |
| `/{slug}` | 调用完整 Skill（像 ta 一样跟你聊天） |
| `/{slug}-memory` | 回忆模式（帮你回忆那些事） |
| `/{slug}-persona` | 仅人物性格 |
| `/lingxi-rollback {slug} {version}` | 回滚到历史版本 |
| `/delete-lingxi {slug}` | 删除 |

---

## 效果示例

> 输入：`妈妈，50多岁，退休教师，ENFJ，巨蟹座，唠叨但很温暖，做饭很好吃`

**场景一：日常聊天**

```
用户      ❯ 今天加班到好晚

灵犀 ❯ 又加班？你们公司怎么回事
       吃饭了没有
       别跟我说又吃外卖
```

**场景二：低落时的陪伴**

```
用户      ❯ 唉，最近压力好大

灵犀 ❯ 怎么了
       跟我说说
       不想说也没关系，早点睡
       明天我给你打电话
```

**场景三：开心时的回应**

```
用户      ❯ 我升职了！！！

灵犀 ❯ 真的吗！！！
       太好了我就知道你可以的
       晚上吃点好的庆祝一下
       回来我给你做你爱吃的红烧肉
```

**场景四：纠正模式**

```
用户      ❯ 我妈不会这么冷静，她应该先唠叨我半小时

灵犀 ❯ 好的，我记住了
       [已更新：妈妈在用户压力大时会先唠叨再关心]
```

---

## 功能特性

### 支持的关系类型

| 类型 | 说明 |
|------|------|
| 朋友 | 好友、闺蜜、兄弟、室友、同学... |
| 恋人 | 女友、男友、老婆、老公、前任... |
| 家人 | 爸妈、兄弟姐妹、爷爷奶奶、亲戚... |
| 同事 | 老板、下属、搭档、前辈... |
| 师长 | 老师、导师、教练... |
| 其他 | 任何你在乎的人 |

### 数据源

| 来源 | 格式 | 备注 |
|------|------|------|
| 微信聊天记录 | WeChatMsg / 留痕 / PyWxDump 导出 | 推荐，信息最丰富 |
| QQ 聊天记录 | txt / mht 导出 | 适合学生时代 |
| 朋友圈/微博 | 截图 | 提取公开人设 |
| 照片 | JPEG/PNG（含 EXIF） | 提取时间线和地点 |
| 口述/粘贴 | 纯文本 | 你的主观记忆 |

### 四层架构

| 层 | 名称 | 内容 |
|----|------|------|
| **Part A** | Relationship Memory | 共同经历、互动模式、关键事件、inside jokes |
| **Part B** | Persona | 5 层性格结构：硬规则 → 身份 → 说话风格 → 情感模式 → 关系行为 |
| **Part C** | Emotion Engine | 情绪感知 + 情感映射表 + 温度控制 |
| **Part D** | Long-term Memory | 跨会话记忆累积，越聊越懂你 |

运行逻辑：
```
收到消息 → Part B 判断 ta 会怎么回 → Part C 感知用户情绪 → Part A 补充共同记忆 → Part D 自然融入 → 输出
```

### 核心技术

* **情感 NLP**：实时感知用户情绪状态，调整回应的温度和方式
* **LoRA 持续学习**：通过对话中的纠正和反馈，不断校准人格模型
* **长期记忆**：跨会话记忆累积，参考 [mem0](https://github.com/mem0ai/mem0) 的自适应记忆设计

### 支持的标签

**性格标签**：话痨 · 闷骚 · 嘴硬心软 · 冷暴力 · 粘人 · 独立 · 社牛 · 社恐 · 学霸 · 吃货 · 养生 · 浪漫主义 · 实用主义 · 完美主义 · 拖延症 · 工作狂 · 控制欲 · 秒回选手 · 已读不回 …

**星座**：十二星座全支持

**MBTI**：16 型全支持

### 进化机制

* **追加记忆** → 找到更多聊天记录/照片 → 自动分析增量 → merge 进对应部分
* **对话纠正** → 说「ta不会这样说」→ 写入 Correction 层，立即生效（LoRA 微调）
* **长期积累** → 每次对话自动提取值得记住的信息，越聊越懂你
* **版本管理** → 每次更新自动存档，支持回滚

---

## 项目结构

```
create-lingxi/
├── SKILL.md                # skill 入口
├── prompts/                # Prompt 模板
│   ├── intake.md           #   对话式信息录入
│   ├── memory_analyzer.md  #   关系记忆提取
│   ├── persona_analyzer.md #   性格行为提取（含标签翻译表）
│   ├── memory_builder.md   #   memory.md 生成模板
│   ├── persona_builder.md  #   persona.md 五层结构模板
│   ├── emotion_engine.md   #   情感引擎（情绪感知 + 映射）
│   ├── long_term_memory.md #   长期记忆管理
│   ├── merger.md           #   增量 merge 逻辑
│   ├── correction_handler.md # 对话纠正处理
│   ├── scene_director.md   #   多人场景模式
│   └── session_summary.md  #   对话记忆持久化
├── tools/                  # Python 工具
│   ├── wechat_parser.py    #   微信聊天记录解析
│   ├── qq_parser.py        #   QQ 聊天记录解析
│   ├── social_parser.py    #   社交媒体内容解析
│   ├── photo_analyzer.py   #   照片元信息分析
│   ├── emotion_analyzer.py #   情感分析器
│   ├── skill_writer.py     #   Skill 文件管理
│   └── version_manager.py  #   版本存档与回滚
├── companions/             # 生成的灵犀 Skill（gitignored）
├── docs/
├── requirements.txt
└── LICENSE
```

---

## 注意事项

* **聊天记录质量决定还原度**：微信导出 + 口述 > 仅口述
* 建议优先提供：**日常互动** > **关键时刻** > **冲突/和好**（最能体现真实性格）
* 灵犀会通过纠正机制持续学习，越用越像
* 所有数据仅本地存储，不上传任何服务器
* 本项目基于https://github.com/therealXiaomanChu/ex-skill 进行二次开发，增强了长记忆

### 写在最后

每个人都是独一无二的。ta 的口头禅、ta 生气时的样子、ta 安慰你的方式——这些细微的东西构成了一个人。

灵犀要做的，就是把这些碎片拼起来，让在意的人不再只是记忆里的一个名字。

## License / 许可证

This project is licensed under the MIT License.

Original Copyright (c) 2026 therealXiaomanChu  
Modifications Copyright (c) 2026 LPZ55556

See the [LICENSE](./LICENSE) file for details.

本项目基于 MIT License 开源。原始代码版权归 therealXiaomanChu 所有，修改部分版权归 LPZ55556 所有。详细内容请查看 [LICENSE](./LICENSE) 文件。

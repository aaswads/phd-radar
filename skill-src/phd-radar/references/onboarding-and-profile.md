# Onboarding and persistent profile

Use this reference when no saved profile exists, when the user asks what information is needed, or when the user changes defaults.

## First-use conversation

Do not begin a broad search with an empty profile. Give the user one copyable reply block and show which values are required:

```text
这是首次使用。请直接复制下面内容并填写；不确定的项目可以留空，我会使用下方默认值。你的回复将作为确认，并保存为以后自动复用的永久配置。

目标地区（必填，例如：荷兰、德国、北欧、英国）：
研究主题（必填，例如：Human-AI Interaction、AI Agent Evaluation、Human Factors）：
QS 目标学科（推荐，例如：Computer Science and Information Systems、Psychology）：
申请背景（推荐：当前/最高学历、专业、毕业时间）：
方法与技能（推荐：用户实验、统计、Python、LLM/Agent evaluation）：
应用领域（可选：航空、自动驾驶、安全关键系统）：
语言与资格限制（可选：英语、是否接受需当地语言岗位）：
最早入学时间（可选）：
必须排除（可选）：
也可以直接提供 CV；仍请明确目标地区和研究主题。
```

Read the executable defaults with `python scripts/profile_store.py defaults`, then show them in a compact list:

- opportunity types: PhD, doctoral researcher, doctoral candidate;
- funding: salaried or fully funded only;
- deadline: exclude expired; exclude unknown deadline from formal recommendations;
- discovery: configured sources plus regional open Web discovery, followed by official-page verification;
- QS overall maximum: 300 inclusive;
- QS subject maximum: 100 inclusive; top 50 preferred; any configured subject may pass;
- ranking edition: latest official edition available;
- unranked institution: manual review;
- lab review window: five years;
- lab signals: recent research, ERC/MSCA, doctoral outputs/destinations, external collaboration;
- output language: Chinese;
- dashboard: one overall 10-point score only.
- formal result target: 20; broad discovery roster target: about 60 candidates;
- application routes: specific advertised positions plus verified funded-program routes.

Present recommended terms as examples, not assumed facts. Useful topic vocabulary includes `Human-AI Interaction`, `AI Agent Evaluation`, `Agent Harness`, `Human Factors`, `Trust in Automation`, `Safety-Critical Systems`, `HCI`, and `LLM Evaluation`. Useful method vocabulary includes `user study`, `mixed methods`, `experiment design`, `statistics`, `Python`, `R`, `eye tracking`, and `simulation`. Map user wording to canonical terms while retaining the original wording in `profile_notes`. When the user's research topic could map to multiple QS subjects, show the candidate official labels and ask one focused follow-up.

## First save

Build a complete profile from the reply and executable defaults. The onboarding text makes the user's filled reply the confirmation to persist. Save it with `python scripts/profile_store.py set <profile.json>`, read it back, and show a compact saved summary. The first profile becomes `default`; subsequent searches reuse it automatically.

If the environment has no writable local state, return the exact proposed JSON and explain that persistence is pending. Never claim a profile was saved without reading it back successfully.

## Later changes

Interpret “修改配置/以后改成/默认增加/移除” as a persistent patch. Show only changed fields plus their old and new values, confirm, patch the profile, and read it back. Interpret “这次/本轮/临时” as a one-off override and leave the profile unchanged.

Useful conversational examples:

- “以后地区加上瑞士和比利时。”
- “把 QS 总榜门槛改成 200，CS 学科仍保留前 100。”
- “默认研究方向增加 agent harness 和 agent evaluation。”
- “这次只查北欧，不修改我的配置。”
- “以后不考虑需要德语的岗位。”

At the start of each later search, echo only the high-impact profile values and any one-off overrides. Offer “你可以直接说‘修改配置：……’” rather than repeating the full onboarding form.

Completion: a first-time user sees required inputs, recommended vocabulary, and all defaults; a confirmed first profile is saved and read back; later persistent patches and one-off overrides remain distinguishable.

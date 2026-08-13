# PhD Radar

[English](README.md) | **简体中文**

PhD Radar 是一个面向 Codex 的博士职位搜索技能，用于发现、核验、筛选、评分并展示有薪或全额资助的博士机会。它结合定向职位来源与开放网络检索，并在结果进入排名前，返回大学、研究机构、雇主、项目或官方申请页面进行核验。

## 功能

- 保存并复用搜索配置，包括地区、研究主题、方法、资助要求和排除条件。
- 发现公开招聘的博士职位和带资助的博士项目通道。
- 使用官方来源核验职位信息。
- 根据可配置条件筛选学校和研究团队。
- 按 0-10 分对已核验结果进行评分和排序。
- 生成独立、可离线打开的卡片式 HTML 仪表盘。

## 安装

克隆仓库，然后将 `skill-src/phd-radar` 复制到 Codex 的技能目录：

```powershell
git clone https://github.com/aaswads/phd-radar.git
Copy-Item -Recurse .\phd-radar\skill-src\phd-radar "$HOME\.codex\skills\phd-radar"
```

重启 Codex 或新建一个任务，让 Codex 重新发现技能。之后可以这样使用：

> 使用 PhD Radar，帮我寻找欧洲方向与机器学习相关的全额资助博士职位。

首次使用时，技能会引导你建立一份可复用的搜索配置。

## 仓库结构

```text
skill-src/phd-radar/
|-- SKILL.md
|-- agents/openai.yaml
|-- assets/
|-- examples/
|-- references/
`-- scripts/
```

随附的 Python 脚本仅依赖标准库，用于保存搜索配置、执行确定性排名和生成仪表盘。

## 校验

在仓库根目录执行：

```powershell
python "$HOME\.codex\skills\.system\skill-creator\scripts\quick_validate.py" .\skill-src\phd-radar
python .\skill-src\phd-radar\scripts\rank_results.py --self-test
```

## 数据与核验说明

PhD Radar 默认将用户搜索配置保存在用户自己的 Codex 目录中。个人配置、生成的仪表盘和搜索结果不会包含在本仓库内。博士职位信息可能发生变化，申请前请始终以链接指向的官方申请页面为准。

## 开源许可证

本项目采用 [MIT License](LICENSE)。

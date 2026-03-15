# HSR QA Automation (Skeleton) / 星穹铁道测试自动化（骨架）

本项目提供一套轻量、无第三方依赖（仅 Python 标准库）的自动化测试骨架，用于类似《崩坏：星穹铁道》的客户端进行端到端的健康检查/冒烟/回归验证。
This project contains a lightweight, dependency-free (stdlib-only) automation harness intended for end-to-end sanity/smoke/regression checks of a game client like Honkai: Star Rail.

核心代码位于 `qa/`。
The core implementation lives under `qa/`.

## Quick Start / 快速开始

1) Create a config / 创建配置
- Copy `qa/config.example.json` to `qa/config.json` and fill paths.
- 复制 `qa/config.example.json` 为 `qa/config.json`，并填写真实路径。

2) Run a suite / 运行套件
```powershell
python qa/run.py --config qa/config.json --suite smoke
```

3) View report / 查看报告
- `qa/out/latest/report.html`

## Docs / 文档
- `qa/README.md`: QA harness usage and notes / 自动化骨架使用说明与注意事项
- `qa/hsrqa/adapters/README.md`: Adapter integrations (ADB/Appium/perf/network) / 适配器扩展说明


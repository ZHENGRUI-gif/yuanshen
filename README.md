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

## PC E2E (UI) / PC 端到端（UI）

该项目支持通过 AutoHotkey（可选依赖）在 PC 上跑登录/主界面/战斗/抽卡/重连等流程自动化。
This project can run PC UI end-to-end flows (login/main/battle/gacha/reconnect) via AutoHotkey (optional dependency).

1) Install AutoHotkey / 安装 AutoHotkey
- Set `pc.ahk_exe` in `qa/config.json`.
- 在 `qa/config.json` 中配置 `pc.ahk_exe`（AutoHotkey64.exe 路径）。

2) Prepare templates / 准备模板图
- Put templates under `qa/assets/templates/` (see `qa/assets/templates/README.md`).
- 将模板图放到 `qa/assets/templates/`（见 `qa/assets/templates/README.md`）。

3) Run suite / 运行套件
```powershell
python qa/run.py --config qa/config.json --suite pc_e2e
```

4) (Optional) Disconnect/reconnect / （可选）断网重连
- Set `network.allow_disruptive=true` and adjust interface name in `qa/suites/pc_e2e.json`.
- 在配置里设置 `network.allow_disruptive=true`，并在 `qa/suites/pc_e2e.json` 里改网卡名（如 WLAN/Ethernet）。

## Docs / 文档
- `qa/README.md`: QA harness usage and notes / 自动化骨架使用说明与注意事项
- `qa/hsrqa/adapters/README.md`: Adapter integrations (ADB/Appium/perf/network) / 适配器扩展说明
- `qa/flows/README.md`: PC flow scripts / PC 流程脚本说明

# HSR QA Automation (Skeleton) / 星穹铁道测试自动化（骨架）

本目录提供一套轻量、无第三方依赖（仅 Python 标准库）的自动化测试骨架，用于类似《崩坏：星穹铁道》的客户端进行端到端的健康检查/冒烟/回归验证。
This folder contains a lightweight, dependency-free (stdlib-only) automation harness intended for end-to-end sanity/smoke/regression checks of a game client like Honkai: Star Rail.

## 能力范围 / What It Can Do (No Extra Tools)
- 启动/退出游戏进程（Windows PC）。 / Start/stop the game process (PC Windows).
- 采集基础运行信号（退出码、运行时长）。 / Capture basic runtime signals (exit code, runtime duration).
- 收集日志并扫描崩溃特征。 / Collect logs and scan for crash signatures.
- 运行 JSON 定义的套件（smoke/regression）。 / Run suites (smoke/regression) defined in JSON.
- 生成简易 HTML 报告。 / Produce a simple HTML report.

## 可扩展方向 / Designed To Plug Into Later
- ADB/Appium（Android/iOS）设备控制。 / ADB/Appium (Android/iOS) device control.
- 弱网/丢包等网络模拟（外部工具）。 / Network shaping (weak network, packet loss) via external tooling.
- 崩溃 dump 符号化、性能追踪、埋点/遥测接入。 / Crash dump symbolication, perf tracing, and telemetry ingestion.

## 快速开始 / Quick Start

1) 创建配置 / Create a config
- 复制 `qa/config.example.json` 为 `qa/config.json`，并填写真实路径。 / Copy `qa/config.example.json` to `qa/config.json` and fill paths.

2) 运行套件 / Run a suite
```powershell
python qa/run.py --config qa/config.json --suite smoke
```

3) 查看报告 / View report
- `qa/out/latest/report.html`

## 说明 / Notes
- 本骨架默认偏保守：不会主动执行可能影响系统全局状态的命令（例如改防火墙/全局网络规则）。 / The harness is intentionally conservative: it will not run destructive system commands (e.g., changing firewall rules).
- 若要做移动端自动化：实现 `qa/hsrqa/adapters/adb_adapter.py` 与 `qa/hsrqa/adapters/appium_adapter.py`，并在套件里接入。 / For mobile automation, implement `qa/hsrqa/adapters/adb_adapter.py` and `qa/hsrqa/adapters/appium_adapter.py` and wire them into suites.

# Adapters / 适配器

适配器用于对接标准库之外的设备控制与外部工具（可选）。
Adapters are optional integrations for controlling devices or tooling not available via stdlib.

## 建议适配器 / Suggested Adapters
- `adb_adapter.py`：Android 安装/启动/logcat/拉取文件。 / Android install/launch/logcat/pull.
- `appium_adapter.py`：Android/iOS 的 UI 自动化。 / UI automation for Android/iOS.
- `perf_adapter.py`：FPS/内存等性能采集（如 PresentMon、Perfetto、Xcode Instruments）。 / FPS/memory capture (e.g., PresentMon, Perfetto, Xcode Instruments).
- `network_adapter.py`：弱网模拟（仅在配置明确启用且获得授权的前提下）。 / Weak network simulation via approved tooling.

## 安全约束 / Safety
- 保持副作用可控：除非在配置中显式开启，否则不要修改系统级全局网络/防火墙规则。 / Keep adapters side-effect safe: do not change global system network rules unless explicitly enabled in config.

# Adapters

Adapters are optional integrations for controlling devices or tooling not available via stdlib.

Suggested adapters:
- `adb_adapter.py`: Android install/launch/logcat/pull.
- `appium_adapter.py`: UI automation for Android/iOS.
- `perf_adapter.py`: FPS/memory capture (e.g., PresentMon, Perfetto, Xcode Instruments).
- `network_adapter.py`: Weak network simulation via approved tooling.

Keep adapters side-effect safe: do not change global system network rules unless explicitly enabled in config.


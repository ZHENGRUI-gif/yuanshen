# PC Flows (AutoHotkey) / PC 流程脚本（AutoHotkey）

这里存放 PC 端 UI 自动化流程脚本（可选依赖 AutoHotkey）。
These are Windows UI automation flow scripts for the PC client (optional dependency: AutoHotkey).

## Prerequisites / 前置条件
- Install AutoHotkey and set `pc.ahk_exe` in `qa/config.json`.
- 安装 AutoHotkey，并在 `qa/config.json` 中配置 `pc.ahk_exe`（AutoHotkey64.exe 的路径）。

## Templates / 模板图片
- Put template images under `qa/assets/templates/` and keep filenames stable.
- 将模板图片放到 `qa/assets/templates/`，并保持文件名稳定（脚本会引用）。

## How To Run / 如何运行
- Use step type `pc.ahk.run_script` in suites, pointing to scripts here.
- 在 suite 里使用 `pc.ahk.run_script`，并把 `script` 指向本目录脚本。


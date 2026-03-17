; AutoHotkey v1 script (template).
; PC E2E flow: login -> main UI -> battle -> gacha -> disconnect/reconnect handling.
;
; IMPORTANT:
; - You must capture and provide template images in qa/assets/templates/
; - Tune coordinates and timeouts per your resolution and game UI version.
; - Exit code 0 = PASS, non-zero = FAIL.

#NoEnv
SendMode Input
SetWorkingDir %A_ScriptDir%
SetTitleMatchMode, 2

; ---- Configurable paths (repo-relative) ----
templates := A_ScriptDir . "\..\assets\templates\"

; Example templates you should provide:
tpl_login_btn := templates . "login_btn.png"
tpl_enter_game := templates . "enter_game.png"
tpl_main_ui := templates . "main_ui_anchor.png"
tpl_battle_start := templates . "battle_start.png"
tpl_battle_auto := templates . "battle_auto.png"
tpl_battle_end := templates . "battle_end.png"
tpl_gacha_entry := templates . "gacha_entry.png"
tpl_gacha_once := templates . "gacha_once.png"
tpl_gacha_result := templates . "gacha_result.png"
tpl_reconnect := templates . "reconnect.png"

; ---- Helpers ----
FindAndClick(tpl, timeoutMs := 30000) {
    start := A_TickCount
    Loop {
        ImageSearch, fx, fy, 0, 0, A_ScreenWidth, A_ScreenHeight, %tpl%
        if (ErrorLevel = 0) {
            Click, %fx%, %fy%
            return true
        }
        if (A_TickCount - start > timeoutMs) {
            return false
        }
        Sleep, 500
    }
}

WaitFor(tpl, timeoutMs := 30000) {
    start := A_TickCount
    Loop {
        ImageSearch, fx, fy, 0, 0, A_ScreenWidth, A_ScreenHeight, %tpl%
        if (ErrorLevel = 0) {
            return true
        }
        if (A_TickCount - start > timeoutMs) {
            return false
        }
        Sleep, 500
    }
}

Fail(msg) {
    FileAppend, %msg%`n, *STDERR*
    ExitApp, 2
}

; ---- Flow ----
; 1) Login / 登录
if (!FindAndClick(tpl_login_btn, 60000)) {
    Fail("login_btn not found")
}
Sleep, 1000
if (!WaitFor(tpl_enter_game, 60000)) {
    ; Some clients skip this step; allow to continue if main UI shows up.
}

; 2) Enter main UI / 进入主界面
; You may need to click "Enter Game" then wait for a main UI anchor.
FindAndClick(tpl_enter_game, 30000)
if (!WaitFor(tpl_main_ui, 120000)) {
    Fail("main_ui not detected")
}

; 3) Run one battle / 跑一场战斗
if (!FindAndClick(tpl_battle_start, 60000)) {
    Fail("battle_start not found")
}
Sleep, 2000
; Optional: enable auto
FindAndClick(tpl_battle_auto, 10000)
if (!WaitFor(tpl_battle_end, 300000)) {
    Fail("battle_end not detected")
}
Sleep, 1000

; 4) Gacha once / 抽卡一次
if (!FindAndClick(tpl_gacha_entry, 60000)) {
    Fail("gacha_entry not found")
}
Sleep, 2000
if (!FindAndClick(tpl_gacha_once, 60000)) {
    Fail("gacha_once not found")
}
if (!WaitFor(tpl_gacha_result, 60000)) {
    Fail("gacha_result not detected")
}

; 5) Disconnect/Reconnect / 断网重连
; Network toggle is handled by the Python runner step `pc.network.toggle_interface`.
; Here we only verify reconnect dialog can be handled if it appears.
if (WaitFor(tpl_reconnect, 5000)) {
    FindAndClick(tpl_reconnect, 10000)
    if (!WaitFor(tpl_main_ui, 120000)) {
        Fail("reconnect failed: main_ui not detected")
    }
}

ExitApp, 0


@echo off
rem Execute SCons inside this project's uv-managed Python virtual environment.
set hereOrig=%~dp0
set here=%hereOrig%
if #%hereOrig:~-1%# == #\# set here=%hereOrig:~0,-1%
powershell -ExecutionPolicy Bypass -NoProfile -File "%here%\ensureuv.ps1" run --directory "%here%" SCons %*

@echo off
for /l %%x in (1, 1, 14) do (
    start "Router %%x" python Router.py
)
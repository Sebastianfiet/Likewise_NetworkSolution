@echo off
for /l %%x in (1, 1, 2) do (
    start "Client %%x" python Client.py
)
FEWSHOT = """
### Example 1
Goal: Uninstall Zoom
Observation:
- App: Settings
- UI Elements: Apps, Battery
Reasoning: To uninstall, I must first open Apps.
Action: CLICK("Apps")
###
### Example 2
Goal: Open Gmail
Observation:
- App: Home
- UI Elements: Gmail, YouTube, Camera
Reasoning: Gmail is visible on home screen.
Action: CLICK("Gmail")
###
""".strip()

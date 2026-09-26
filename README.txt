HYDRO BUDDY — WINDOWS EXE BUILDER
=================================

This project builds the Hydro Buddy desktop reminder app as a standalone
Windows .exe using GitHub Actions. You do NOT need Python installed on your PC.

WHAT YOU GET
------------
- HydroBuddy.exe (single Windows executable)
- Bottom-right animated reminder popup
- Uploaded mascot animation
- Male / Female mascot selector
- Reminder interval: 15 / 30 / 45 / 60 minutes
- Popup duration: 30 / 45 / 60 / 90 / 120 seconds
- 1-minute test reminder
- Water / Move / Sound toggles
- X close + Dismiss buttons

BUILD INSTRUCTIONS (NO PYTHON NEEDED ON YOUR PC)
------------------------------------------------
1. Create or sign in to a GitHub account.
2. Create a NEW repository. Public is simplest for this personal project.
3. Open the repository.
4. Click "Add file" -> "Upload files".
5. Upload ALL files and folders from this project, including:
      hydro_buddy.py
      mascot_male.gif
      mascot_female.gif
      requirements.txt
      .github/workflows/build-windows.yml
6. Commit the files.
7. Open the "Actions" tab in the repository.
8. Click "Build Hydro Buddy Windows EXE" on the left.
9. Click "Run workflow" -> "Run workflow".
10. Wait for the green check mark.
11. Open the completed workflow run.
12. Scroll to "Artifacts".
13. Download "HydroBuddy-Windows".
14. Extract the downloaded ZIP.
15. Run "HydroBuddy.exe" on Windows.

IMPORTANT
---------
- You do NOT need to install Python on your Windows PC.
- The build happens on GitHub's Windows runner.
- Windows may show a SmartScreen warning for a newly built unsigned app.
  That can happen because the EXE is not code-signed.
- The app is designed as a portable EXE; it does not need Python installed.

IF YOU GET STUCK
----------------
Send me a screenshot of the GitHub page where you are stuck and I will tell
you exactly what to click next.

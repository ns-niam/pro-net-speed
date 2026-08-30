# ProNet Speed

A lightweight Windows network monitoring application that displays real-time
download and upload speeds directly on the desktop.

## Features

- Real-time download speed monitoring
- Real-time upload speed monitoring
- Peak download speed tracking
- Peak upload speed tracking
- Daily network data usage monitoring
- Total downloaded data tracking
- Total uploaded data tracking
- Detailed network statistics
- Windows system tray support
- Always on Top option
- Lightweight background operation

## Microsoft Store

ProNet Speed has been prepared and submitted for publication on the Microsoft Store.

Store category:
Utilities & tools → Backup + manage

Target platform:
Windows 10/11

Package format:
MSIX

The application uses the `runFullTrust` capability because it is a desktop
application that requires full-trust access to run as a native Windows
application and provide system-level desktop and system tray functionality.

## Development History

This project was developed as a Windows desktop network monitoring application.

Main development work completed:

- Designed the real-time network speed monitoring system
- Implemented download and upload speed tracking
- Added peak speed tracking
- Added daily and total data usage statistics
- Implemented system tray functionality
- Added Always on Top functionality
- Created and configured the MSIX package
- Prepared Microsoft Store assets and screenshots
- Added privacy policy and support information
- Completed Microsoft Store age ratings
- Configured worldwide availability and pricing
- Submitted the application for Microsoft Store certification

## Project Setup

Clone the repository:

git clone <YOUR_REPOSITORY_URL>

Open the project:

cd ProNet-Speed

Install the required dependencies using the project's requirements/configuration
files.

## Requirements

Before running or developing the project again, install all required
dependencies.

If this project uses Python:

pip install -r requirements.txt

If new dependencies are added during future development, update
`requirements.txt` before pushing changes to GitHub.

To generate/update the requirements file:

pip freeze > requirements.txt

Important:
Review the generated file before committing it. Only required project
dependencies should ideally be included.

## Future Development

Potential improvements:

- Network usage history
- Weekly and monthly usage reports
- Graphs and visual analytics
- Network adapter selection
- Internet connection status detection
- Custom speed display themes
- Startup with Windows option
- Export usage statistics
- Notifications for unusual network activity
- Improved Microsoft Store screenshots and promotional assets

## Important Files

- `README.md` — Project documentation and development notes
- `requirements.txt` — Python dependencies, if applicable
- Project source code — Main application logic
- Package configuration — Windows/MSIX packaging configuration
- App assets — Icons, screenshots, and Store assets

## Before Deleting the Development Environment

Before deleting the GitHub Codespace, verify that:

- All latest source code has been pushed to GitHub
- README.md is committed and pushed
- requirements.txt is committed and pushed
- MSIX/package configuration files are included
- Important assets and icons are committed
- `.gitignore` is configured correctly
- No important local-only changes remain uncommitted
- The application can be rebuilt from the GitHub repository

## Backup Strategy

GitHub is the primary source of truth for this project.

Do not rely on the deleted Codespace as a backup.

Before making major changes in the future:

1. Pull the latest code from GitHub
2. Create a new branch for major features
3. Update requirements when dependencies change
4. Update README when architecture or features change
5. Commit and push regularly

## Developer

Developed by Niam

Website:
https://nsniam.dev

## License

Copyright © 2026 Niam. All rights reserved.
python -m ruff check . --fix
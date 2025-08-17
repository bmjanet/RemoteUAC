# RemoteUAC
A remote, context-aware UAC (User Account Control) system that mirrors how Duo or other MFA systems handle secure logins, but for admin privilege escalation and program installations.

The project is a work-in-progress. Currently, the goal is to complete the backend/client-side code so that it can intercept the Windows API for requesting admin privilege escalation, and send the metadata from the application to be installed/run to the admin user's phone.

---
render_macros: true
---

# DMGBuild {{ release }}

## What is this?

DMGBuild is a command line tool to create macOS disk images (aka `.dmg` files). While it is possible to create disk images easily enough from the command line using the `hdiutil` program that ships with macOS, there is no easy way to configure the appearance of the resulting disk image when the user opens it. Some people have used AppleScript to automate Finder to adjust the appearance, but since Finder saves its `.DS_Store` files asynchronously, it is hard to guarantee that the changes will actually be saved when you want them to be. It also means that you need a GUI session, with Finder running, in order to build your disk image.

DMGBuild does not rely on Finder; nor does it rely on deprecated APIs (like the Alias Manager functions). Instead, it uses the `ds_store` and `mac_alias` Python modules, which know how to construct the relevant data in Python code.

As DMGBuild is a wrapper around macOS specific tools, it can't be used on Windows or Linux.

## Contents

- [Usage](usage.md)
- [Settings](settings.md)
- [Example Settings File](example.md)

[app]
title = AETHER
package.name = aether
package.domain = org.aether

source.dir = .
source.include_exts = py,png,jpg,jpeg,kv,atlas,json,txt,wav,mp3

version = 0.1
requirements = python3,kivy

orientation = portrait
fullscreen = 0

android.permissions = INTERNET,RECORD_AUDIO
android.api = 35
android.minapi = 23
android.archs = arm64-v8a

[buildozer]
log_level = 2
warn_on_root = 1

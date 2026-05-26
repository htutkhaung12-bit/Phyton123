[app]
title = KM DGSK WINGO PRO
package.name = kmdgskwingopro
package.domain = org.kmdgsk.sniper
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 19.3.1

requirements = python3,kivy,kivymd,requests,urllib3,certifi,idna,charset-normalizer

orientation = portrait
fullscreen = 0

android.archs = arm64-v8a, armeabi-v7a
android.allow_backup = True
android.permissions = INTERNET, READ_PHONE_STATE

android.api = 33
android.minapi = 21
android.ndk = 25b
android.ndk_api = 21

android.private_storage = True
android.skip_update = False
android.accept_sdk_license = True
p4a.branch = master

[buildozer]
log_level = 2
warn_on_root = 1

[app]

# (၁) App ၏ အခြေခံ အချက်အလက်များ
title = KM DGSK WINGO PRO
package.name = kmdgskwingopro
package.domain = org.kmdgsk.sniper
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 19.3.1

# (၂) Libraries များ (ဗားရှင်း အသေမကန့်သတ်ဘဲ Engine ကို အလိုအလျောက် ရှာခိုင်းသည့် စနစ်)
requirements = python3,kivy,kivymd,requests,urllib3,certifi,idna,charset-normalizer

# (၃) မျက်နှာပြင် အနေအထား
orientation = portrait
fullscreen = 0

# (၄) Architecture နှင့် Permissions
android.archs = arm64-v8a, armeabi-v7a
android.allow_backup = True
android.permissions = INTERNET, READ_PHONE_STATE

# (၅) Android SDK / NDK (လက်ရှိ GitHub Actions နှင့် အကိုက်ညီဆုံး ဗားရှင်းများ)
android.api = 33
android.minapi = 21
android.ndk_api = 21

# (၆) Buildozer Engine Core Settings
android.private_storage = True
android.skip_update = False
android.accept_sdk_license = True

[buildozer]
log_level = 2
warn_on_root = 1

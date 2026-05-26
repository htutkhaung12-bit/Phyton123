[app]

# (၁) App ၏ အခြေခံ အချက်အလက်များ
title = KM DGSK WINGO PRO
package.name = kmdgskwingopro
package.domain = org.kmdgsk.sniper
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 19.3.1

# (၂) အဓိက လိုအပ်သော Libraries များ (ထပ်မပြင်ရအောင် ကွက်တိထည့်ထားသည်)
requirements = python3,kivy==2.3.0,kivymd==1.2.0,requests,urllib3,certifi,idna,charset-normalizer

# (၃) မျက်နှာပြင် အနေအထား သတ်မှတ်ချက်
orientation = portrait
fullscreen = 0

# (၄) Android Architecture သတ်မှတ်ချက်
android.archs = arm64-v8a, armeabi-v7a
android.allow_backup = True

# (၅) ⚠️ အင်တာနက်နှင့် ဖုန်းအခြေအနေ ဖတ်ခွင့် ပေးခြင်း (လိုင်စင်နှင့် Bot အတွက် မရှိမဖြစ်)
android.permissions = INTERNET, READ_PHONE_STATE

# (၆) Android SDK / NDK ဗားရှင်း သတ်မှတ်ချက်များ (ကျစ်လစ်ပြီး အမှားကင်းစေရန်)
android.api = 33
android.minapi = 21
android.ndk = 25b
android.ndk_api = 21

# (၇) Buildozer Engine အတွက် လိုအပ်သော သီးသန့် Settings များ
android.private_storage = True
android.skip_update = False
android.accept_sdk_license = True
p4a.branch = master

[buildozer]
log_level = 2

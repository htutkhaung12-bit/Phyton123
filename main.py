import time
import datetime
import threading
from kivy.config import Config

# WebView နှင့် Screen ကြိုတင်ပြင်ဆင်မှုများ
Config.set('kivy', 'log_level', 'info')

from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.dialog import MDDialog
from kivymd.uix.menu import MDDropdownMenu
from kivy.clock import Clock

# --- 🛡️ [၁] 1 DEVICE 1 LICENSE SYSTEM ---
# ပိုင်ရှင်ကနေ ကိုယ်ပေးချင်တဲ့ ဖုန်းရဲ့ ANDROID_ID နဲ့ သက်တမ်းကုန်ရက်ကို ဒီမှာ လာဖြည့်ရုံပါပဲ
AUTHORIZED_DEVICES = {
    "PC_TEST_DEVICE_DEBUG_12345": "2026-12-31", # PC မှာ စမ်းသပ်ရန် Debug ID
    "8f92a3b4c5d6e7f8": "2026-06-30",           # နမူနာ ဖုန်း ID ထည့်ရန်နေရာ
}

# Android စနစ်အစစ်ပေါ်တွင် Run လျှင် ဖုန်းရဲ့ သီးသန့် Device ID ကို ဆွဲထုတ်မည့်စနစ်
def get_android_id():
    try:
        from jnius import autoclass
        Secure = autoclass('android.provider.Settings$Secure')
        PythonActivity = autoclass('org.kivy.android.PythonActivity')
        activity = PythonActivity.mActivity
        contentResolver = activity.getContentResolver()
        return Secure.getString(contentResolver, Secure.ANDROID_ID)
    except:
        return "PC_TEST_DEVICE_DEBUG_12345"

def get_license_days_left(expire_date_str):
    try:
        expire_date = datetime.datetime.strptime(expire_date_str, "%Y-%m-%d").date()
        today = datetime.date.today()
        days_left = (expire_date - today).days
        return max(0, days_left)
    except:
        return 0

# --- 🎨 [၂] SCREEN MANAGEMENTS ---
class WindowManager(ScreenManager):
    pass

class LicenseScreen(Screen):
    def on_enter(self):
        Clock.schedule_once(self.check_license, 1.5)

    def check_license(self, dt):
        app = MDApp.get_running_app()
        app.my_device_id = get_android_id()
        
        if app.my_device_id in AUTHORIZED_DEVICES:
            expire_str = AUTHORIZED_DEVICES[app.my_device_id]
            days = get_license_days_left(expire_str)
            if days > 0:
                app.days_left = days
                self.manager.current = 'main_menu'
                return
        
        self.ids.status_lbl.text = f"❌ ခွင့်ပြုချက်မရှိသော စက်ပစ္စည်း ဖြစ်သည်!\nDevice ID: {app.my_device_id}"
        self.ids.status_lbl.text_color = (0.9, 0.2, 0.2, 1)

class MainMenuScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.menu = None

    def on_enter(self):
        app = MDApp.get_running_app()
        self.ids.license_lbl.text = f"Premium Licensed Version | သက်တမ်းကျန်ရက်: {app.days_left} ရက်"
        self.setup_dropdown()

    def setup_dropdown(self):
        menu_items = [
            {"text": "6 Lottery", "viewclass": "OneLineListItem", "on_release": lambda x="6 Lottery": self.set_site(x)},
            {"text": "CK Lottery", "viewclass": "OneLineListItem", "on_release": lambda x="CK Lottery": self.set_site(x)},
        ]
        self.menu = MDDropdownMenu(caller=self.ids.site_drop, items=menu_items, width_mult=4)

    def set_site(self, site_name):
        self.ids.site_drop.text = site_name
        self.menu.dismiss()
        # 6 Lottery အတွက် အခြေခံလောင်းကြေး ၁၀၀၊ CK Lottery အတွက် ၁၀ အလိုအလျောက် သတ်မှတ်ခြင်း
        if site_name == "6 Lottery":
            self.ids.amt_input.text = "100"
        else:
            self.ids.amt_input.text = "10"

    def confirm_start_bot(self):
        site = self.ids.site_drop.text
        if site == "ဝဘ်ဆိုဒ်ရွေးချယ်ရန် 👇":
            return
            
        app = MDApp.get_running_app()
        app.bot_settings = {
            "site": site,
            "base_bet": int(self.ids.amt_input.text),
            "profit": int(self.ids.profit_input.text),
            "loss": int(self.ids.loss_input.text),
            "url": "https://www.6win999.com/#/register?invitationCode=32613664268" if site == "6 Lottery" else "http://www.cklottery.info/#/register?invitationCode=55655490677"
        }

        # ⚠️ WARNING CONFIRMATION BOX (ဟုတ်ပြီ / ပြန်ပြင်မယ် ခလုတ်စနစ်)
        self.dialog = MDDialog(
            title="⚠️ အတည်ပြုရန် သတိပေးချက်",
            text=f"သင်သည် {site} သို့ ဝင်ရောက်ပြီး Bot မောင်းနှင်တော့မည် ဖြစ်သည်။\n\nလောင်းကြေး၊ အမြတ်၊ အရှုံးငွေ သေချာသတ်မှတ်ပြီးပြီလား?",
            buttons=[
                MDFlatButton(text="ပြန်ပြင်မယ်", text_color=(0.9, 0.2, 0.2, 1), on_release=lambda x: self.dialog.dismiss()),
                MDRaisedButton(text="ဟုတ်ပြီ", md_bg_color=(0.15, 0.68, 0.37, 1), on_release=self.launch_engine)
            ],
        )
        self.dialog.open()

    def launch_engine(self, instance):
        self.dialog.dismiss()
        self.manager.current = 'bot_running'

class BotRunningScreen(Screen):
    def on_enter(self):
        app = MDApp.get_running_app()
        self.ids.bot_title.text = f"🤖 {app.bot_settings['site']} SNIPER ACTIVE"
        app.is_running = True
        threading.Thread(target=self.run_bot_core, daemon=True).start()

    def run_bot_core(self):
        app = MDApp.get_running_app()
        settings = app.bot_settings
        
        # UI Log အခြေအနေကို လှမ်းပြောင်းပေးမည့် စနစ်
        def update_log(text):
            Clock.schedule_once(lambda dt: setattr(self.ids.log_box, 'text', self.ids.log_box.text + f"\n{text}"))

        update_log(f"[စနစ်] KOMIN {{DGSK}} ဖန်တီးသည့် အင်ဂျင် စတင်နေပြီ...\n[လိုင်း] {settings['url']} သို့ ချိတ်ဆက်နေပါသည်...\n\n=== ကျေးဇူးပြု၍ App အတွင်း ဂိမ်းထဲဝင်ပေးပါ ===")
        
        total_p_l = 0
        
        # 🎰 ဤနေရာတွင် မင်းရဲ့ Wingo 30s Algorithm (Dragon/Ping-pong Logic) များ ဆက်လက်လည်ပတ်ပါမည်
        while app.is_running:
            # ဥပမာအဖြစ် Target ပြည့်သွားလျှင် ရပ်တန့်မည့် သရုပ်ပြစနစ်
            time.sleep(5)
            # စမ်းသပ်ရန် ပွဲစဉ်အောင်မြင်မှု Log အတုပြခြင်း
            total_p_l += settings['base_bet'] * 1.5
            Clock.schedule_once(lambda dt: setattr(self.ids.pl_lbl, 'text', f"အမြတ်ငွေ P/L = {total_p_l} MMK"))
            update_log(f"[✨ WIN] Sniper ပစ်လွှတ်မှု အောင်မြင်သည်။ လက်ရှိရလဒ်: {total_p_l}")

            if total_p_l >= settings['profit']:
                app.is_running = False
                Clock.schedule_once(lambda dt: self.show_target_reached_dialog(total_p_l))
                break

    def show_target_reached_dialog(self, final_p_l):
        # ⚠️ TARGET ရောက်သွားလျှင် ပြသပေးမည့် WARNING BOX လှလှလေး
        self.target_dialog = MDDialog(
            title="🎯 TARGET REACHED!",
            text=f"သတ်မှတ်ချက် ရောက်ရှိသွားသဖြင့် စနစ်ကို ဘေးကင်းစွာ ရပ်တန့်လိုက်ပါပြီ။\n\nစုစုပေါင်း ရလဒ်: {final_p_l} MMK",
            buttons=[MDRaisedButton(text="ပင်မစာမျက်နှာသို့", md_bg_color=(0.11, 0.52, 0.93, 1), on_release=self.go_back_to_menu)]
        )
        self.target_dialog.open()

    def go_back_to_menu(self, instance):
        self.target_dialog.dismiss()
        self.manager.current = 'main_menu'

# --- 🏗️ [၃] MAIN APPLICATION CLASS ---
class WinGoSniperApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.days_left = 0
        self.my_device_id = ""
        self.bot_settings = {}
        self.is_running = False

    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Amber"
        
        from kivy.lang import Builder
        return Builder.load_string('''
WindowManager:
    LicenseScreen:
        name: 'license'
    MainMenuScreen:
        name: 'main_menu'
    BotRunningScreen:
        name: 'bot_running'

<LicenseScreen>:
    MDBoxLayout:
        orientation: 'vertical'
        padding: 20
        spacing: 20
        md_bg_color: 0.05, 0.05, 0.07, 1
        
        MDLabel:
            text: "🎰 KM (DGSK) WIN GO PRO 🎰"
            font_style: "H4"
            halign: "center"
            theme_text_color: "Custom"
            text_color: 1, 0.8, 0, 1
            bold: True
            
        MDLabel:
            id: status_lbl
            text: "📡 လိုင်စင်စနစ်အား စစ်ဆေးနေပါသည်..."
            font_style: "Subtitle1"
            halign: "center"
            theme_text_color: "Custom"
            text_color: 1, 1, 1, 1

<MainMenuScreen>:
    MDBoxLayout:
        orientation: 'vertical'
        padding: 15
        spacing: 12
        md_bg_color: 0.08, 0.08, 0.1, 1
        
        MDLabel:
            text: "🎰 KM (DGSK) WIN GO PRO SNIPER 🎰"
            font_style: "H5"
            halign: "center"
            theme_text_color: "Custom"
            text_color: 1, 0.8, 0, 1
            bold: True
            
        MDLabel:
            text: "KOMIN {DGSK} ဖန်တီးသည်"
            font_style: "Caption"
            halign: "center"
            theme_text_color: "Secondary"
            bold: True

        MDLabel:
            id: license_lbl
            text: "Premium Licensed Version"
            font_style: "Caption"
            halign: "center"
            theme_text_color: "Custom"
            text_color: 0.95, 0.77, 0.06, 1
            bold: True

        MDRaisedButton:
            id: site_drop
            text: "ဝဘ်ဆိုဒ်ရွေးချယ်ရန် 👇"
            pos_hint: {'center_x': .5}
            size_hint_x: 0.9
            on_release: root.menu.open()
            md_bg_color: 0.15, 0.15, 0.2, 1

        MDTextField:
            id: amt_input
            hint_text: "အခြေခံလောင်းကြေး (MMK)"
            mode: "rectangle"
            text: "100"
            size_hint_x: 0.9
            pos_hint: {'center_x': .5}

        MDTextField:
            id: profit_input
            hint_text: "အမြတ်ရည်မှန်းချက် (MMK)"
            mode: "rectangle"
            text: "5000"
            size_hint_x: 0.9
            pos_hint: {'center_x': .5}

        MDTextField:
            id: loss_input
            hint_text: "အရှုံးခံနိုင်ရည်သတ်မှတ်ချက် (MMK)"
            mode: "rectangle"
            text: "5000"
            size_hint_x: 0.9
            pos_hint: {'center_x': .5}

        MDRaisedButton:
            text: "🚀 START BOT ENGINE"
            font_size: "18sp"
            size_hint_x: 0.9
            size_hint_y: 0.07
            pos_hint: {'center_x': .5}
            md_bg_color: 0.15, 0.68, 0.37, 1
            on_release: root.confirm_start_bot()

<BotRunningScreen>:
    MDBoxLayout:
        orientation: 'vertical'
        padding: 15
        spacing: 10
        md_bg_color: 0.05, 0.05, 0.05, 1
        
        MDLabel:
            id: bot_title
            text: "🤖 SNIPER RUNNING ACTIVE"
            font_style: "H6"
            halign: "center"
            theme_text_color: "Custom"
            text_color: 0, 1, 0, 1
            bold: True
            
        MDLabel:
            id: bal_lbl
            text: "လက်ကျန်ငွေ = တွက်ချက်ဆဲ..."
            font_style: "Subtitle1"
            theme_text_color: "Custom"
            text_color: 0.18, 0.8, 0.44, 1
            
        MDLabel:
            id: pl_lbl
            text: "အမြတ်ငွေ P/L = 0.0 MMK"
            font_style: "Subtitle1"
            theme_text_color: "Custom"
            text_color: 0.95, 0.77, 0.06, 1

        ScrollView:
            size_hint_y: 0.6
            md_bg_color: 0, 0, 0, 1
            MDLabel:
                id: log_box
                text: ""
                font_style: "Body2"
                theme_text_color: "Custom"
                text_color: 0, 1, 0, 1
                size_hint_y: None
                height: self.texture_size[1]
                halign: "left"
                valign: "top"
''')

if __name__ == '__main__':
    WinGoSniperApp().run()


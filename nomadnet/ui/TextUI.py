import os
import platform

import RNS
import urwid

from nomadnet import NomadNetworkApp
from nomadnet.ui.textui import *

COLORMODE_MONO = 1
COLORMODE_16   = 16
COLORMODE_88   = 88
COLORMODE_256  = 256
COLORMODE_TRUE = 2**24
THEME_DARK     = 0x01
THEME_LIGHT    = 0x02

THEMES = {
    THEME_DARK: {
        "urwid_theme": [
            # Style name                    # 16-color style                        # Monochrome style          # 88, 256 and true-color style
            ("heading",                     "light gray,underline", "default",      "underline",                "g93,underline", "default"),
            ("menubar",                     "black", "light gray",                  "standout",                 "#111", "#bbb"),
            ("scrollbar",                   "light gray", "default",                "default",                  "#444", "default"),
            ("shortcutbar",                 "black", "light gray",                  "standout",                 "#111", "#bbb"),
            ("body_text",                   "light gray", "default",                "default",                  "#ddd", "default"),
            ("error_text",                  "dark red", "default",                  "default",                  "dark red", "default"),
            ("warning_text",                "yellow", "default",                    "default",                  "#ba4", "default"),
            ("inactive_text",               "dark gray", "default",                 "default",                  "dark gray", "default"),
            ("buttons",                     "light green,bold", "default",          "default",                  "#00a533", "default"),
            ("msg_editor",                  "black", "light cyan",                  "standout",                 "#111", "#0bb"),
            ("msg_header_ok",               "black", "light green",                 "standout",                 "#111", "#6b2"),
            ("msg_header_caution",          "black", "yellow",                      "standout",                 "#111", "#fd3"),
            ("msg_header_sent",             "black", "light gray",                  "standout",                 "#111", "#ddd"),
            ("msg_header_propagated",       "black", "light blue",                  "standout",                 "#111", "#28b"),
            ("msg_header_delivered",        "black", "light blue",                  "standout",                 "#111", "#28b"),
            ("msg_header_failed",           "black", "dark gray",                   "standout",                 "#000", "#777"),
            ("msg_warning_untrusted",       "black", "dark red",                    "standout",                 "#111", "dark red"),
            ("list_focus",                  "black", "light gray",                  "standout",                 "#111", "#aaa"),
            ("list_off_focus",              "black", "dark gray",                   "standout",                 "#111", "#777"),
            ("list_trusted",                "dark green", "default",                "default",                  "#6b2", "default"),
            ("list_focus_trusted",          "black", "light gray",                  "standout",                 "#150", "#aaa"),
            ("list_unknown",                "dark gray", "default",                 "default",                  "#bbb", "default"),
            ("list_normal",                 "dark gray", "default",                 "default",                  "#bbb", "default"),
            ("list_untrusted",              "dark red", "default",                  "default",                  "#a22", "default"),
            ("list_focus_untrusted",        "black", "light gray",                  "standout",                 "#810", "#aaa"),
            ("list_unresponsive",           "yellow", "default",                    "default",                  "#b92", "default"),
            ("list_focus_unresponsive",     "black", "light gray",                  "standout",                 "#530", "#aaa"),
            ("topic_list_normal",           "light gray", "default",                "default",                  "#ddd", "default"),
            ("browser_controls",            "light gray", "default",                "default",                  "#bbb", "default"),
            ("progress_full",               "black", "light gray",                  "standout",                 "#111", "#bbb"),
            ("progress_empty",              "light gray", "default",                "default",                  "#ddd", "default"),
            ("interface_title",             "", "",                                 "default",                  "", ""),
            ("interface_title_selected",    "bold", "",                             "bold",                     "", ""),
            ("connected_status",            "dark green", "default",                "default",                  "dark green", "default"),
            ("disconnected_status",         "dark red", "default",                  "default",                  "dark red", "default"),
            ("placeholder",                 "dark gray", "default",                 "default",                  "dark gray", "default"),
            ("placeholder_text",            "dark gray", "default",                 "default",                  "dark gray", "default"),
            ("error",                       "light red,blink",                      "default", "blink",         "#f44,blink", "default"),

        ],
    },
    THEME_LIGHT: {
        "urwid_theme": [
            # Style name                    # 16-color style                        # Monochrome style          # 88, 256 and true-color style
            ("heading",                     "dark gray,underline", "default",      "underline",                "g93,underline", "default"),
            ("menubar",                     "black", "dark gray",                  "standout",                 "#111", "#bbb"),
            ("scrollbar",                   "dark gray", "default",                "default",                  "#444", "default"),
            ("shortcutbar",                 "black", "dark gray",                  "standout",                 "#111", "#bbb"),
            ("body_text",                   "dark gray", "default",                "default",                  "#222", "default"),
            ("error_text",                  "dark red", "default",                 "default",                  "dark red", "default"),
            ("warning_text",                "yellow", "default",                   "default",                  "#ba4", "default"),
            ("inactive_text",               "light gray", "default",               "default",                  "dark gray", "default"),
            ("buttons",                     "light green,bold", "default",         "default",                  "#00a533", "default"),
            ("msg_editor",                  "black", "dark cyan",                  "standout",                 "#111", "#0bb"),
            ("msg_header_ok",               "black", "dark green",                 "standout",                 "#111", "#6b2"),
            ("msg_header_caution",          "black", "yellow",                     "standout",                 "#111", "#fd3"),
            ("msg_header_sent",             "black", "dark gray",                  "standout",                 "#111", "#ddd"),
            ("msg_header_propagated",       "black", "light blue",                 "standout",                 "#111", "#28b"),
            ("msg_header_delivered",        "black", "light blue",                 "standout",                 "#111", "#28b"),
            ("msg_header_failed",           "black", "dark gray",                  "standout",                 "#000", "#777"),
            ("msg_warning_untrusted",       "black", "dark red",                   "standout",                 "#111", "dark red"),
            ("list_focus",                  "black", "dark gray",                  "standout",                 "#111", "#aaa"),
            ("list_off_focus",              "black", "dark gray",                  "standout",                 "#111", "#777"),
            ("list_trusted",                "dark green", "default",               "default",                  "#4a0", "default"),
            ("list_focus_trusted",          "black", "dark gray",                  "standout",                 "#150", "#aaa"),
            ("list_unknown",                "dark gray", "default",                "default",                  "#444", "default"),
            ("list_normal",                 "dark gray", "default",                "default",                  "#444", "default"),
            ("list_untrusted",              "dark red", "default",                 "default",                  "#a22", "default"),
            ("list_focus_untrusted",        "black", "dark gray",                  "standout",                 "#810", "#aaa"),
            ("list_unresponsive",           "yellow", "default",                   "default",                  "#b92", "default"),
            ("list_focus_unresponsive",     "black", "light gray",                 "standout",                 "#530", "#aaa"),
            ("topic_list_normal",           "dark gray", "default",                "default",                  "#222", "default"),
            ("browser_controls",            "dark gray", "default",                "default",                  "#444", "default"),
            ("progress_full",               "black", "dark gray",                  "standout",                 "#111", "#bbb"),
            ("progress_empty",              "dark gray", "default",                "default",                  "#ddd", "default"),
            ("interface_title",             "dark gray", "default",                "default",                  "#444", "default"),
            ("interface_title_selected",    "dark gray,bold", "default",           "bold",                     "#444,bold", "default"),
            ("connected_status",            "dark green", "default",               "default",                  "#4a0", "default"),
            ("disconnected_status",         "dark red", "default",                 "default",                  "#a22", "default"),
            ("placeholder",                 "light gray", "default",               "default",                  "#999", "default"),
            ("placeholder_text",            "light gray", "default",               "default",                  "#999", "default"),
            ("error",                       "dark red,blink", "default",           "blink",                    "#a22,blink", "default"),
        ],
    }
}

GLYPHSETS = {
    "plain": 1,
    "unicode": 2,
    "nerdfont": 3
}

if platform.system() == "Darwin":
    urm_char = " \uf0e0"
    ur_char = "\uf0e0 "
else:
    urm_char = " \uf003"
    ur_char = "\uf003 "

GLYPHS = {
    # Glyph name        # Plain      # Unicode      # Nerd Font
    ("check",           "=",         "\u2713",      "\u2713"),
    ("cross",           "X",         "\u2715",      "\u2715"),
    ("unknown",         "?",         "?",           "?"),
    ("encrypted",       "",          "\u26BF",      "\uf023"),
    ("plaintext",       "!",         "!",           "\uf06e "),
    ("arrow_r",         "->",        "\u2192",      "\u2192"),
    ("arrow_l",         "<-",        "\u2190",      "\u2190"),
    ("arrow_u",         "/\\",       "\u2191",      "\u2191"),
    ("arrow_d",         "\\/",       "\u2193",      "\u2193"),
    ("warning",         "!",         "\u26a0",      "\uf12a"),
    ("info",            "i",         "\u2139",      "\U000f064e"),
    ("unread",          "[!]",       "\u2709",      ur_char),
    ("divider1",        "-",         "\u2504",      "\u2504"),
    ("peer",            "[P]",       "\u24c5 ",     "\uf415"),
    ("node",            "[N]",       "\u24c3 ",     "\U000f0002"),
    ("page",            "",          "\u25a4 ",     "\uf719 "),
    ("speed",           "",          "\u25F7 ",     "\U000f04c5 "),
    ("decoration_menu", " +",        " +",          " \U000f043b"),
    ("unread_menu",     " !",        " \u2709",     urm_char),
    ("globe",           "",          "",            "\uf484"),
    ("sent",            "/\\",       "\u2191",      "\U000f0cd8"),
    ("papermsg",        "P",         "\u25a4",      "\uf719"),
    ("qrcode",          "QR",        "\u25a4",      "\uf029"),
    ("selected",        "[*] ",      "\u25CF",      "\u25CF"),
    ("unselected",      "[ ] ",      "\u25CB",      "\u25CB"),
}

class TextUI:

    def __init__(self):
        self.restore_ixon = False

        try:
            # Check if ixon is already disabled
            result = subprocess.run(["stty", "-a"], capture_output=True, text=True, check=True)
            if "-ixon" in result.stdout:
                pass
            else:
                subprocess.run(["stty", "-ixon"], check=True)
                self.restore_ixon = True

        except Exception as e:
            RNS.log("Could not configure terminal flow control sequences, some keybindings may not work.", RNS.LOG_WARNING)
            RNS.log("The contained exception was: "+str(e))

        self.app = NomadNetworkApp.get_shared_instance()
        self.app.ui = self
        self.loop = None

        urwid.set_encoding("UTF-8")

        intro_timeout  = self.app.config["textui"]["intro_time"]
        colormode      = self.app.config["textui"]["colormode"]
        theme          = self.app.config["textui"]["theme"]
        mouse_enabled  = self.app.config["textui"]["mouse_enabled"]

        self.palette   = THEMES[theme]["urwid_theme"]

        if self.app.config["textui"]["glyphs"] == "plain":
            glyphset = "plain"
        elif self.app.config["textui"]["glyphs"] == "unicode":
            glyphset = "unicode"
        elif self.app.config["textui"]["glyphs"] == "nerdfont":
            glyphset = "nerdfont"
        else:
            glyphset = "unicode"

        self.glyphs = {}
        for glyph in GLYPHS:
            self.glyphs[glyph[0]] = glyph[GLYPHSETS[glyphset]]

        self.screen = urwid.raw_display.Screen()
        self.screen.register_palette(self.palette)

        self.main_display = Main.MainDisplay(self, self.app)

        if intro_timeout > 0:
            self.intro_display = Extras.IntroDisplay(self.app)
            initial_widget = self.intro_display.widget
        else:
            initial_widget = self.main_display.widget

        self.loop = urwid.MainLoop(initial_widget, unhandled_input=self.unhandled_input, screen=self.screen, handle_mouse=mouse_enabled)

        if intro_timeout > 0:
            self.loop.set_alarm_in(intro_timeout, self.display_main)

        if "KONSOLE_VERSION" in os.environ:
            if colormode > 16:
                RNS.log("", RNS.LOG_WARNING, _override_destination = True)
                RNS.log("", RNS.LOG_WARNING, _override_destination = True)
                RNS.log("You are using the terminal emulator Konsole.", RNS.LOG_WARNING, _override_destination = True)
                RNS.log("If you are not seeing the user interface, it is due to a bug in Konsole/urwid.", RNS.LOG_WARNING, _override_destination = True)
                RNS.log("", RNS.LOG_WARNING, _override_destination = True)

                RNS.log("To circumvent this, use another terminal emulator, or launch nomadnet within a", RNS.LOG_WARNING, _override_destination = True)
                RNS.log("screen session, using a command like the following:", RNS.LOG_WARNING, _override_destination = True)
                RNS.log("", RNS.LOG_WARNING, _override_destination = True)
                RNS.log("screen nomadnet", RNS.LOG_WARNING, _override_destination = True)
                RNS.log("", RNS.LOG_WARNING, _override_destination = True)
                RNS.log("Press ctrl-c to exit now and try again.", RNS.LOG_WARNING, _override_destination = True)

        self.set_colormode(colormode)

        self.main_display.start()
        self.loop.run()

    def set_colormode(self, colormode):
        self.colormode = colormode
        self.screen.set_terminal_properties(colormode)

        if self.colormode < 256:
            self.screen.reset_default_terminal_palette()
            self.restore_palette = True

    def unhandled_input(self, key):
        if key == "ctrl q":
            raise urwid.ExitMainLoop
        elif key == "ctrl e":
            pass

    def display_main(self, loop, user_data):
        self.loop.widget = self.main_display.widget

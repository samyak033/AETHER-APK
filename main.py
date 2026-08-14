from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.progressbar import ProgressBar
from kivy.uix.scrollview import ScrollView
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle

from datetime import datetime
import json
import os


class AetherApp(App):

    def build(self):

        # =========================
        # SETTINGS
        # =========================

        self.goal_seconds = 6 * 60 * 60
        self.seconds = 0
        self.running = False
        self.timer_event = None

        self.today = datetime.now().strftime(
            "%Y-%m-%d"
        )

        self.save_file = os.path.join(
            self.user_data_dir,
            "study_history.json"
        )

        self.load_today()

        # =========================
        # MAIN
        # =========================

        main = BoxLayout(
            orientation="vertical",
            padding=12,
            spacing=8
        )

        # Background
        with main.canvas.before:

            Color(
                0.01,
                0.01,
                0.03,
                1
            )

            self.background = Rectangle(
                pos=main.pos,
                size=main.size
            )

        main.bind(
            pos=self.update_background,
            size=self.update_background
        )

        # =========================
        # HEADER
        # =========================

        header = BoxLayout(
            orientation="vertical",
            size_hint_y=None,
            height=95
        )

        title = Label(
            text="🤖 AETHER",
            font_size=34,
            bold=True,
            color=(0.1, 0.6, 1, 1)
        )

        header.add_widget(title)

        self.clock_label = Label(
            text="00:00:00",
            font_size=16
        )

        header.add_widget(
            self.clock_label
        )

        main.add_widget(header)

        # =========================
        # STUDY INFO
        # =========================

        study_box = BoxLayout(
            orientation="vertical",
            size_hint_y=None,
            height=125
        )

        self.timer_label = Label(
            text="Study: 00:00:00",
            font_size=25,
            bold=True,
            color=(0.1, 0.7, 1, 1)
        )

        study_box.add_widget(
            self.timer_label
        )

        self.remaining_label = Label(
            text="🎯 Remaining: 06:00:00",
            font_size=15
        )

        study_box.add_widget(
            self.remaining_label
        )

        self.progress = ProgressBar(
            max=100,
            value=0,
            size_hint_y=None,
            height=18
        )

        study_box.add_widget(
            self.progress
        )

        self.progress_label = Label(
            text="0% of today's goal",
            font_size=14
        )

        study_box.add_widget(
            self.progress_label
        )

        main.add_widget(
            study_box
        )

        # =========================
        # CHAT AREA
        # =========================

        self.scroll = ScrollView(
            do_scroll_x=False
        )

        self.chat = BoxLayout(
            orientation="vertical",
            spacing=8,
            padding=8,
            size_hint_y=None
        )

        self.chat.bind(
            minimum_height=self.chat.setter(
                "height"
            )
        )

        self.scroll.add_widget(
            self.chat
        )

        main.add_widget(
            self.scroll
        )

        # Welcome message

        self.add_message(
            "AETHER",
            "Hello! I'm AETHER 🤖\n"
            "How can I help you today?"
        )

        # =========================
        # INPUT
        # =========================

        input_box = BoxLayout(
            size_hint_y=None,
            height=50,
            spacing=6
        )

        self.command_box = TextInput(
            hint_text="Type a message...",
            multiline=False,
            font_size=16
        )

        self.command_box.bind(
            on_text_validate=self.send_command
        )

        input_box.add_widget(
            self.command_box
        )

        send = Button(
            text="SEND",
            size_hint_x=None,
            width=90,
            background_normal="",
            background_color=(
                0.02,
                0.35,
                0.7,
                1
            )
        )

        send.bind(
            on_press=self.send_command
        )

        input_box.add_widget(
            send
        )

        main.add_widget(
            input_box
        )

        # =========================
        # STUDY BUTTONS
        # =========================

        buttons = BoxLayout(
            size_hint_y=None,
            height=48,
            spacing=5
        )

        start = Button(
            text="▶ START"
        )

        start.bind(
            on_press=self.start_study
        )

        buttons.add_widget(start)

        pause = Button(
            text="⏸ PAUSE"
        )

        pause.bind(
            on_press=self.pause_study
        )

        buttons.add_widget(pause)

        history = Button(
            text="📊 HISTORY"
        )

        history.bind(
            on_press=self.show_history
        )

        buttons.add_widget(history)

        main.add_widget(
            buttons
        )

        # =========================
        # CLOCK
        # =========================

        Clock.schedule_interval(
            self.update_clock,
            1
        )

        self.update_display()

        return main

    # ==================================================
    # BACKGROUND
    # ==================================================

    def update_background(
        self,
        instance,
        value
    ):

        self.background.pos = instance.pos
        self.background.size = instance.size

    # ==================================================
    # CHAT MESSAGE
    # ==================================================

    def add_message(
        self,
        sender,
        message
    ):

        label = Label(
            text=f"{sender}: {message}",
            font_size=15,
            halign="left",
            valign="top",
            size_hint_y=None,
            text_size=(None, None),
            padding=(8, 8)
        )

        label.bind(
            texture_size=lambda obj, size:
            setattr(
                obj,
                "height",
                size[1] + 16
            )
        )

        label.bind(
            width=lambda obj, width:
            setattr(
                obj,
                "text_size",
                (width - 16, None)
            )
        )

        self.chat.add_widget(
            label
        )

        Clock.schedule_once(
            self.scroll_bottom,
            0.1
        )

    # ==================================================
    # SCROLL
    # ==================================================

    def scroll_bottom(self, dt):

        self.scroll.scroll_y = 0

    # ==================================================
    # CLOCK
    # ==================================================

    def update_clock(self, dt):

        self.clock_label.text = datetime.now().strftime(
            "%I:%M:%S %p"
        )

    # ==================================================
    # COMMAND
    # ==================================================

    def send_command(self, instance):

        command = (
            self.command_box.text
            .strip()
            .lower()
        )

        if not command:
            return

        # Show user message

        self.add_message(
            "YOU",
            command
        )

        # =========================
        # HELLO
        # =========================

        if (
            "hello" in command
            or "hi" in command
        ):

            answer = (
                "Hello! 🤖 Nice to see you."
            )

        # =========================
        # TIME
        # =========================

        elif "time" in command:

            answer = (
                "The current time is "
                + datetime.now().strftime(
                    "%I:%M:%S %p"
                )
            )

        # =========================
        # DATE
        # =========================

        elif "date" in command:

            answer = (
                "Today is "
                + datetime.now().strftime(
                    "%d %B %Y"
                )
            )

        # =========================
        # START
        # =========================

        elif (
            "start" in command
            and "stud" in command
        ) or command == "start":

            self.start_study(None)

            answer = (
                "Study session started! 📚🔥"
            )

        # =========================
        # PAUSE
        # =========================

        elif (
            "pause" in command
            and "stud" in command
        ) or command == "pause":

            self.pause_study(None)

            answer = (
                "Study session paused. ⏸️"
            )

        # =========================
        # RESET
        # =========================

        elif "reset" in command:

            self.reset_study(None)

            answer = (
                "Today's timer was reset."
            )

        # =========================
        # STUDY TIME
        # =========================

        elif (
            "study time" in command
            or "how much" in command
            or "how long" in command
        ):

            hours = self.seconds // 3600

            minutes = (
                self.seconds % 3600
            ) // 60

            seconds = self.seconds % 60

            answer = (
                f"You studied "
                f"{hours:02d}:"
                f"{minutes:02d}:"
                f"{seconds:02d} today. 📚"
            )

        # =========================
        # HISTORY
        # =========================

        elif "history" in command:

            self.show_history(None)

            answer = (
                "I've opened your study history. 📊"
            )

        # =========================
        # HELP
        # =========================

        elif (
            "help" in command
            or "what can you do" in command
        ):

            answer = (
                "I can currently:\n"
                "📚 Track your study time\n"
                "📊 Show study history\n"
                "⏱️ Tell the time\n"
                "📅 Tell the date\n"
                "🤖 Respond to commands"
            )

        # =========================
        # UNKNOWN
        # =========================

        else:

            answer = (
                "I don't understand that yet 🤔\n"
                "Try asking 'help'."
            )

        self.add_message(
            "AETHER",
            answer
        )

        self.command_box.text = ""

    # ==================================================
    # START STUDY
    # ==================================================

    def start_study(self, instance):

        if not self.running:

            self.running = True

            self.timer_event = (
                Clock.schedule_interval(
                    self.count_study,
                    1
                )
            )

    # ==================================================
    # PAUSE
    # ==================================================

    def pause_study(self, instance):

        self.running = False

        if self.timer_event:

            self.timer_event.cancel()

            self.timer_event = None

        self.save_today()

    # ==================================================
    # RESET
    # ==================================================

    def reset_study(self, instance):

        self.running = False

        if self.timer_event:

            self.timer_event.cancel()

            self.timer_event = None

        self.seconds = 0

        self.save_today()

        self.update_display()

    # ==================================================
    # TIMER
    # ==================================================

    def count_study(self, dt):

        self.seconds += 1

        self.update_display()

        if self.seconds % 5 == 0:

            self.save_today()

    # ==================================================
    # DISPLAY
    # ==================================================

    def update_display(self):

        hours = self.seconds // 3600

        minutes = (
            self.seconds % 3600
        ) // 60

        seconds = self.seconds % 60

        self.timer_label.text = (
            f"Study: "
            f"{hours:02d}:"
            f"{minutes:02d}:"
            f"{seconds:02d}"
        )

        remaining = max(
            0,
            self.goal_seconds - self.seconds
        )

        r_hours = remaining // 3600

        r_minutes = (
            remaining % 3600
        ) // 60

        r_seconds = remaining % 60

        self.remaining_label.text = (
            f"🎯 Remaining: "
            f"{r_hours:02d}:"
            f"{r_minutes:02d}:"
            f"{r_seconds:02d}"
        )

        percentage = (
            self.seconds /
            self.goal_seconds
        ) * 100

        percentage = min(
            100,
            percentage
        )

        self.progress.value = percentage

        self.progress_label.text = (
            f"{percentage:.1f}% of today's goal"
        )

    # ==================================================
    # SAVE
    # ==================================================

    def save_today(self):

        data = {}

        if os.path.exists(
            self.save_file
        ):

            try:

                with open(
                    self.save_file,
                    "r"
                ) as file:

                    data = json.load(file)

            except:

                data = {}

        data[self.today] = self.seconds

        try:

            with open(
                self.save_file,
                "w"
            ) as file:

                json.dump(
                    data,
                    file,
                    indent=4
                )

        except Exception as error:

            print(
                "Save error:",
                error
            )

    # ==================================================
    # LOAD
    # ==================================================

    def load_today(self):

        if not os.path.exists(
            self.save_file
        ):

            return

        try:

            with open(
                self.save_file,
                "r"
            ) as file:

                data = json.load(file)

            self.seconds = data.get(
                self.today,
                0
            )

        except:

            self.seconds = 0

    # ==================================================
    # HISTORY
    # ==================================================

    def show_history(self, instance):

        if not os.path.exists(
            self.save_file
        ):

            self.add_message(
                "AETHER",
                "No study history yet."
            )

            return

        try:

            with open(
                self.save_file,
                "r"
            ) as file:

                data = json.load(file)

            if not data:

                self.add_message(
                    "AETHER",
                    "No study history yet."
                )

                return

            lines = []

            for date, seconds in sorted(
                data.items(),
                reverse=True
            ):

                try:

                    formatted_date = (
                        datetime.strptime(
                            date,
                            "%Y-%m-%d"
                        ).strftime(
                            "%d %b %Y"
                        )
                    )

                except:

                    formatted_date = date

                hours = seconds // 3600

                minutes = (
                    seconds % 3600
                ) // 60

                secs = seconds % 60

                lines.append(
                    f"{formatted_date}: "
                    f"{hours:02d}:"
                    f"{minutes:02d}:"
                    f"{secs:02d}"
                )

            self.add_message(
                "AETHER",
                "📊 Study History\n"
                + "\n".join(lines)
            )

        except:

            self.add_message(
                "AETHER",
                "Could not load history."
            )


if __name__ == "__main__":
    AetherApp().run()
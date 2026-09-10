"""Interfaz gráfica moderna y visualmente atractiva del chatbot de práctica del verbo TO BE."""

from __future__ import annotations

import datetime
from pathlib import Path
import tkinter as tk
from tkinter import messagebox, scrolledtext

from PIL import Image

try:
    import customtkinter as ctk
    HAS_CTK = True
except ImportError:
    HAS_CTK = False

from validator import validate, extract_valid_name


class ChatbotGUI:
    """Interfaz gráfica principal de BeBot."""

    def __init__(self, root: ctk.CTk | tk.Tk) -> None:
        self.root = root
        self.root.title("BeBot — TO BE Verb Practice Assistant")
        self.root.geometry("820x680")
        self.root.minsize(620, 520)

        self.name: str | None = None
        self._mode: str = "ask_name"
        self._theme_mode: str = "dark"
        self.score: int = 0

        self.avatar_img_path = Path(__file__).parent / "bebot_avatar.png"
        self.header_avatar_img = None
        self.chat_avatar_img = None

        if HAS_CTK and self.avatar_img_path.exists():
            try:
                pil_avatar = Image.open(self.avatar_img_path)
                self.header_avatar_img = ctk.CTkImage(light_image=pil_avatar, dark_image=pil_avatar, size=(46, 46))
                self.chat_avatar_img = ctk.CTkImage(light_image=pil_avatar, dark_image=pil_avatar, size=(36, 36))
            except Exception:
                pass

        if HAS_CTK:
            ctk.set_appearance_mode("dark")
            ctk.set_default_color_theme("blue")
            self._build_ctk_interface()
        else:
            self._build_tk_interface()

        self.root.after(100, self._start_flow)

    # -------------------------------------------------------------------------
    # CUSTOMTKINTER INTERFACE
    # -------------------------------------------------------------------------
    def _build_ctk_interface(self) -> None:
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=1)

        # Main Header Frame Container
        header_container = ctk.CTkFrame(self.root, corner_radius=0, fg_color="transparent")
        header_container.grid(row=0, column=0, sticky="ew")
        header_container.grid_columnconfigure(0, weight=1)

        # Header Main Panel
        self.header = ctk.CTkFrame(header_container, corner_radius=0, fg_color=("gray92", "#111827"), height=76)
        self.header.grid(row=0, column=0, sticky="ew")
        self.header.grid_propagate(False)
        self.header.grid_columnconfigure(1, weight=1)

        # Accent Gradient Line beneath header
        self.header_accent = ctk.CTkFrame(header_container, corner_radius=0, height=2, fg_color="#6366F1")
        self.header_accent.grid(row=1, column=0, sticky="ew")

        # Bot Avatar Icon Badge
        avatar_outer = ctk.CTkFrame(
            self.header,
            width=48,
            height=48,
            corner_radius=24,
            fg_color="transparent" if self.header_avatar_img else "#4F46E5",
        )
        avatar_outer.grid(row=0, column=0, padx=(18, 12), pady=14)
        avatar_outer.grid_propagate(False)
        if self.header_avatar_img:
            lbl_avatar = ctk.CTkLabel(avatar_outer, image=self.header_avatar_img, text="")
        else:
            lbl_avatar = ctk.CTkLabel(avatar_outer, text="🤖", font=ctk.CTkFont(size=24))
        lbl_avatar.place(relx=0.5, rely=0.5, anchor="center")

        # Bot Title & Status Frame
        info_frame = ctk.CTkFrame(self.header, fg_color="transparent")
        info_frame.grid(row=0, column=1, sticky="w", pady=12)

        title_row = ctk.CTkFrame(info_frame, fg_color="transparent")
        title_row.pack(anchor="w")

        title_lbl = ctk.CTkLabel(
            title_row,
            text="BeBot Assistant",
            font=ctk.CTkFont(family="Segoe UI", size=17, weight="bold"),
            text_color=("gray10", "#F9FAFB"),
            anchor="w",
        )
        title_lbl.pack(side="left", anchor="w")

        # Score Badge
        self.score_badge = ctk.CTkFrame(title_row, fg_color=("#E0E7FF", "#312E81"), corner_radius=12)
        self.score_badge.pack(side="left", padx=10)
        self.score_lbl = ctk.CTkLabel(
            self.score_badge,
            text="⭐ Score: 0",
            font=ctk.CTkFont(family="Segoe UI", size=10, weight="bold"),
            text_color=("#3730A3", "#C7D2FE"),
        )
        self.score_lbl.pack(padx=8, pady=2)

        status_lbl = ctk.CTkLabel(
            info_frame,
            text="🟢 Online  ·  Grammar Practice",
            font=ctk.CTkFont(family="Segoe UI", size=11),
            text_color="#10B981",
            anchor="w",
        )
        status_lbl.pack(anchor="w", pady=(1, 0))

        # Header Action Buttons
        actions_frame = ctk.CTkFrame(self.header, fg_color="transparent")
        actions_frame.grid(row=0, column=2, padx=16, pady=14, sticky="e")

        self.theme_btn = ctk.CTkButton(
            actions_frame,
            text="🌙 Mode",
            width=80,
            height=34,
            corner_radius=17,
            fg_color=("gray85", "#1F2937"),
            hover_color=("gray75", "#374151"),
            text_color=("gray10", "#F3F4F6"),
            font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold"),
            command=self._toggle_theme,
        )
        self.theme_btn.pack(side="left", padx=4)

        self.restart_btn = ctk.CTkButton(
            actions_frame,
            text="🔄 Restart",
            width=90,
            height=34,
            corner_radius=17,
            fg_color=("gray85", "#1F2937"),
            hover_color=("gray75", "#374151"),
            text_color=("gray10", "#F3F4F6"),
            font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold"),
            command=self._restart_session,
        )
        self.restart_btn.pack(side="left", padx=4)

        # Chat Area (Scrollable Frame)
        self.chat_frame = ctk.CTkScrollableFrame(
            self.root,
            corner_radius=0,
            fg_color=("gray98", "#0F172A"),
        )
        self.chat_frame.grid(row=1, column=0, sticky="nsew", padx=0, pady=0)
        self.chat_frame.grid_columnconfigure(0, weight=1)

        # Input Footer Bar
        self.footer = ctk.CTkFrame(self.root, fg_color=("gray92", "#111827"), height=76, corner_radius=0)
        self.footer.grid(row=2, column=0, sticky="ew")
        self.footer.grid_columnconfigure(0, weight=1)

        self.entry_var = tk.StringVar()
        self.entry = ctk.CTkEntry(
            self.footer,
            textvariable=self.entry_var,
            placeholder_text="Type an affirmative sentence in English using the verb TO BE (present tense only)...",
            font=ctk.CTkFont(family="Segoe UI", size=13),
            height=48,
            corner_radius=24,
            border_width=1,
            fg_color=("white", "#1E293B"),
            border_color=("gray75", "#334155"),
        )
        self.entry.grid(row=0, column=0, padx=(16, 12), pady=14, sticky="ew")
        self.entry.bind("<Return>", lambda _e: self._on_submit())

        self.send_btn = ctk.CTkButton(
            self.footer,
            text="Send ➔",
            font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
            height=48,
            width=110,
            corner_radius=24,
            fg_color="#6366F1",
            hover_color="#4F46E5",
            command=self._on_submit,
        )
        self.send_btn.grid(row=0, column=1, padx=(0, 16), pady=14)

    def _update_score(self, points: int = 1) -> None:
        self.score += points
        if HAS_CTK:
            self.score_lbl.configure(text=f"⭐ Score: {self.score}")

    def _add_bot_bubble(self, message: str, meta_badge: tuple[str, str] | None = None) -> None:
        row_frame = ctk.CTkFrame(self.chat_frame, fg_color="transparent")
        row_frame.pack(fill="x", padx=20, pady=10, anchor="w")

        avatar = ctk.CTkFrame(
            row_frame,
            width=36,
            height=36,
            corner_radius=18,
            fg_color="transparent" if self.chat_avatar_img else "#6366F1",
        )
        avatar.pack(side="left", anchor="n", padx=(0, 12))
        avatar.pack_propagate(False)
        if self.chat_avatar_img:
            lbl_icon = ctk.CTkLabel(avatar, image=self.chat_avatar_img, text="")
        else:
            lbl_icon = ctk.CTkLabel(avatar, text="🤖", font=ctk.CTkFont(size=18))
        lbl_icon.place(relx=0.5, rely=0.5, anchor="center")

        content_box = ctk.CTkFrame(row_frame, fg_color="transparent")
        content_box.pack(side="left", fill="x", expand=True, anchor="w")

        time_str = datetime.datetime.now().strftime("%H:%M")
        header_lbl = ctk.CTkLabel(
            content_box,
            text=f"BeBot  •  {time_str}",
            font=ctk.CTkFont(family="Segoe UI", size=10, weight="bold"),
            text_color=("gray50", "#94A3B8"),
            anchor="w",
        )
        header_lbl.pack(anchor="w", pady=(0, 3))

        # Card container with left accent line
        card_outer = ctk.CTkFrame(
            content_box,
            fg_color=("white", "#1E293B"),
            border_width=1,
            border_color=("gray85", "#334155"),
            corner_radius=16,
        )
        card_outer.pack(anchor="w")

        # Inner container for text and badges
        card_inner = ctk.CTkFrame(card_outer, fg_color="transparent")
        card_inner.pack(fill="x", expand=True)

        msg_lbl = ctk.CTkLabel(
            card_inner,
            text=message,
            font=ctk.CTkFont(family="Segoe UI", size=13),
            text_color=("gray10", "#F8FAFC"),
            justify="left",
            wraplength=500,
            anchor="w",
        )
        msg_lbl.pack(padx=16, pady=12, anchor="w")

        if meta_badge:
            badge_text, badge_type = meta_badge
            bg_color = ("#D1FAE5", "#064E3B") if badge_type == "valid" else ("#FEE2E2", "#451225")
            txt_color = ("#065F46", "#6EE7B7") if badge_type == "valid" else ("#991B1B", "#FDA4AF")
            border_col = ("#10B981", "#10B981") if badge_type == "valid" else ("#F43F5E", "#F43F5E")

            badge_frame = ctk.CTkFrame(
                card_inner,
                fg_color=bg_color,
                corner_radius=10,
                border_width=1,
                border_color=border_col,
            )
            badge_frame.pack(padx=14, pady=(0, 12), anchor="w")

            badge_lbl = ctk.CTkLabel(
                badge_frame,
                text=badge_text,
                font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold"),
                text_color=txt_color,
            )
            badge_lbl.pack(padx=12, pady=5)

        self._scroll_to_bottom()

    def _add_user_bubble(self, message: str) -> None:
        row_frame = ctk.CTkFrame(self.chat_frame, fg_color="transparent")
        row_frame.pack(fill="x", padx=20, pady=10, anchor="e")

        content_box = ctk.CTkFrame(row_frame, fg_color="transparent")
        content_box.pack(side="right", anchor="e")

        time_str = datetime.datetime.now().strftime("%H:%M")
        user_display = self.name or "You"
        header_lbl = ctk.CTkLabel(
            content_box,
            text=f"{user_display}  •  {time_str}",
            font=ctk.CTkFont(family="Segoe UI", size=10, weight="bold"),
            text_color=("gray50", "#94A3B8"),
            anchor="e",
        )
        header_lbl.pack(anchor="e", pady=(0, 3))

        bubble = ctk.CTkFrame(
            content_box,
            fg_color="#4F46E5",
            corner_radius=18,
        )
        bubble.pack(anchor="e")

        msg_lbl = ctk.CTkLabel(
            bubble,
            text=message,
            font=ctk.CTkFont(family="Segoe UI", size=13),
            text_color="white",
            justify="left",
            wraplength=500,
            anchor="e",
        )
        msg_lbl.pack(padx=16, pady=12, anchor="e")

        avatar = ctk.CTkFrame(row_frame, width=36, height=36, corner_radius=18, fg_color="#10B981")
        avatar.pack(side="right", anchor="n", padx=(12, 0))
        avatar.pack_propagate(False)
        lbl_icon = ctk.CTkLabel(avatar, text="👤", font=ctk.CTkFont(size=18))
        lbl_icon.place(relx=0.5, rely=0.5, anchor="center")

        self._scroll_to_bottom()

    def _scroll_to_bottom(self) -> None:
        self.root.after(20, lambda: self.chat_frame._parent_canvas.yview_moveto(1.0))

    def _toggle_theme(self) -> None:
        if self._theme_mode == "dark":
            ctk.set_appearance_mode("light")
            self._theme_mode = "light"
            self.theme_btn.configure(text="☀️ Mode")
        else:
            ctk.set_appearance_mode("dark")
            self._theme_mode = "dark"
            self.theme_btn.configure(text="🌙 Mode")

    # -------------------------------------------------------------------------
    # FALLBACK TKINTER INTERFACE
    # -------------------------------------------------------------------------
    def _build_tk_interface(self) -> None:
        self.root.configure(bg="#0F172A")
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=1)

        header = tk.Frame(self.root, bg="#1E293B", height=60)
        header.grid(row=0, column=0, sticky="ew")
        tk.Label(
            header,
            text="🤖 BeBot — TO BE Verb Practice Assistant",
            bg="#1E293B",
            fg="#F8FAFC",
            font=("Segoe UI", 14, "bold"),
        ).pack(side="left", padx=15, pady=15)

        self.chat = scrolledtext.ScrolledText(
            self.root,
            bg="#0F172A",
            fg="#F8FAFC",
            font=("Segoe UI", 11),
            wrap=tk.WORD,
            bd=0,
            state=tk.DISABLED,
        )
        self.chat.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

        footer = tk.Frame(self.root, bg="#0F172A")
        footer.grid(row=2, column=0, sticky="ew", padx=10, pady=10)
        footer.columnconfigure(0, weight=1)

        self.entry_var = tk.StringVar()
        self.entry = tk.Entry(footer, textvariable=self.entry_var, font=("Segoe UI", 11))
        self.entry.grid(row=0, column=0, sticky="ew", padx=(0, 8))
        self.entry.bind("<Return>", lambda _e: self._on_submit())

        self.send_btn = tk.Button(footer, text="Send", command=self._on_submit, bg="#6366F1", fg="white")
        self.send_btn.grid(row=0, column=1)

    # -------------------------------------------------------------------------
    # CHATBOT LOGIC
    # -------------------------------------------------------------------------
    def _start_flow(self) -> None:
        msg = "Hello! My name is BeBot. 🤖\nWhat's your name?"
        if HAS_CTK:
            self._add_bot_bubble(msg)
        else:
            self._tk_append(f"BeBot: {msg}\n")
        self._mode = "ask_name"

    def _on_submit(self) -> None:
        raw = self.entry_var.get().strip()
        if not raw:
            return

        if self._mode == "ask_name":
            valid_name = extract_valid_name(raw)
            if not valid_name:
                if HAS_CTK:
                    self._add_user_bubble(raw)
                    self.entry_var.set("")
                    self._add_bot_bubble(
                        "That doesn't seem to be a valid name. 😅\n"
                        "Please tell me your name first (e.g., 'Carlos' or 'My name is Carlos').",
                        meta_badge=("⚠️ Please enter a valid name", "invalid"),
                    )
                else:
                    self._tk_append(f"You: {raw}\n")
                    self._tk_append("BeBot: That doesn't seem to be a valid name. Please enter a valid name.\n")
                    self.entry_var.set("")
                return

            self.name = valid_name
            if HAS_CTK:
                self._add_user_bubble(raw)
                self.entry_var.set("")
                self._add_bot_bubble(
                    f"Nice to meet you, {self.name}! 😊\n\n"
                    "Please type an affirmative sentence in English using the verb TO BE (present tense only)"
                )
            else:
                self._tk_append(f"You: {raw}\n")
                self._tk_append(f"BeBot: Nice to meet you, {self.name}! Please type an affirmative sentence in English using the verb TO BE (present tense only).\n")
                self.entry_var.set("")
            self._mode = "sentence"
            return

        if self._mode == "continue":
            answer = raw.lower()
            if HAS_CTK:
                self._add_user_bubble(raw)
                self.entry_var.set("")
            else:
                self._tk_append(f"You: {raw}\n")
                self.entry_var.set("")

            if answer in {"yes", "y"}:
                msg = "Great! Please write your next sentence."
                if HAS_CTK:
                    self._add_bot_bubble(msg)
                else:
                    self._tk_append(f"BeBot: {msg}\n")
                self._mode = "sentence"
            elif answer in {"no", "n"}:
                self._end_session()
            else:
                msg = "Please answer yes or no."
                if HAS_CTK:
                    self._add_bot_bubble(msg, meta_badge=("⚠️ Please answer yes / no", "invalid"))
                else:
                    self._tk_append(f"BeBot: {msg}\n")
                self._ask_continue()
            return

        # Sentence validation mode
        sentence = raw
        if HAS_CTK:
            self._add_user_bubble(sentence)
            self.entry_var.set("")
        else:
            self._tk_append(f"You: {sentence}\n")
            self.entry_var.set("")

        result = validate(sentence)
        if result.valid:
            self._update_score(1)
            msg = f"Excellent sentence! It matches the structure of '{result.category}'."
            badge = (f"✨ Correct  •  [{result.category}]", "valid")
            if HAS_CTK:
                self._add_bot_bubble(msg, meta_badge=badge)
            else:
                self._tk_append(f"BeBot: ✅ {msg}\n")
        else:
            msg = f"Please check your sentence structure.\n💡 Hint: {result.message}"
            badge = ("⚠️ Invalid Sentence", "invalid")
            if HAS_CTK:
                self._add_bot_bubble(msg, meta_badge=badge)
            else:
                self._tk_append(f"BeBot: ❌ {result.message}\n")

        self._ask_continue()

    def _ask_continue(self) -> None:
        msg = "Do you want to try another sentence? (yes / no)"
        if HAS_CTK:
            self._add_bot_bubble(msg)
        else:
            self._tk_append(f"BeBot: {msg}\n")
        self._mode = "continue"

    def _end_session(self) -> None:
        msg = (
            f"Thanks for practicing with BeBot, {self.name or 'friend'}! 👋\n"
            f"🏆 Final Score: {self.score} valid sentence(s).\n"
            "Keep practicing to master English grammar."
        )
        if HAS_CTK:
            self._add_bot_bubble(msg)
            self.entry.configure(state="disabled")
            self.send_btn.configure(state="disabled")
        else:
            self._tk_append(f"BeBot: {msg}\n")
            self.entry.config(state=tk.DISABLED)
            self.send_btn.config(state=tk.DISABLED)
        self._mode = "ended"

    def _restart_session(self) -> None:
        if HAS_CTK:
            for widget in self.chat_frame.winfo_children():
                widget.destroy()
            self.entry.configure(state="normal")
            self.send_btn.configure(state="normal")
            self.entry_var.set("")
        else:
            self.chat.configure(state=tk.NORMAL)
            self.chat.delete("1.0", tk.END)
            self.chat.configure(state=tk.DISABLED)
            self.entry.configure(state="normal")
            self.send_btn.configure(state="normal")
            self.entry_var.set("")

        self.score = 0
        self._update_score(0)
        self.name = None
        self._mode = "ask_name"
        self._start_flow()
        self.entry.focus_set()

    def _tk_append(self, text: str) -> None:
        if not HAS_CTK:
            self.chat.configure(state=tk.NORMAL)
            self.chat.insert(tk.END, text)
            self.chat.see(tk.END)
            self.chat.configure(state=tk.DISABLED)


def main() -> None:
    try:
        if HAS_CTK:
            root = ctk.CTk()
        else:
            root = tk.Tk()
    except tk.TclError as exc:
        messagebox.showerror(
            "Display Error",
            f"Could not start the graphical interface:\n{exc}",
        )
        raise
    ChatbotGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()

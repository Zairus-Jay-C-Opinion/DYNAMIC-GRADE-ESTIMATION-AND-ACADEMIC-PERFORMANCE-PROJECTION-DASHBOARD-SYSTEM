import tkinter as tk
from tkinter import messagebox, simpledialog

# ── Color palette ──────────────────────────────────────────────
C0 = "#F0F3FA"
C1 = "#D5DEEF"
C2 = "#B1C9EF"
C3 = "#8AAEE0"
C4 = "#638ECB"
C5 = "#395886"
TEXT       = "#1A1A2E"
TEXT_MUTED = "#6B7A99"
SUCCESS    = "#3a9e6f"
WARNING    = "#c4882a"
DANGER     = "#e05555"

FONT_FAMILY = "Segoe UI"

APP_BADGE    = "GMS"
APP_TITLE    = "Grade Monitoring System"
APP_SUBTITLE = "DYNAMIC GRADE TRACKER"

HEADER_ICON_PATH = "assets/icon_grade.jpg"
WINDOW_ICON_PATH = "assets/icon_grade.ico"


class GradeDashboard:

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Grade Monitoring System")
        self.root.geometry("1020x660")
        self.root.minsize(800, 560)
        self.root.configure(bg=C0)

        self.user_id = None
        self.current_subject_id = None
        self.username = "user"
        self.main_frame = None

        self.show_login()

    # ══════════════════════════════════════════════════════════
    # HELPERS
    # ══════════════════════════════════════════════════════════

    def clear_frame(self):
        for w in self.root.winfo_children():
            w.destroy()

    def _ask_string(self, title, prompt):
        self.root.focus_force()
        return simpledialog.askstring(title, prompt, parent=self.root)

    def _ask_float(self, title, prompt):
        self.root.focus_force()
        val = simpledialog.askstring(title, prompt, parent=self.root)
        if val is None:
            return None
        try:
            return float(val)
        except ValueError:
            return None

    def _ask_int(self, title, prompt):
        self.root.focus_force()
        val = simpledialog.askstring(title, prompt, parent=self.root)
        if val is None:
            return None
        try:
            return int(val)
        except ValueError:
            return None

    def _make_header(self, parent, show_user=False):
        header = tk.Frame(parent, bg=C5, height=52)
        header.pack(fill=tk.X, side=tk.TOP)
        header.pack_propagate(False)

        if WINDOW_ICON_PATH:
            try:
                self.root.iconbitmap(WINDOW_ICON_PATH)
            except Exception:
                pass

        badge = tk.Frame(header, bg=C4, width=38, height=38)
        badge.pack(side=tk.LEFT, padx=(14, 10), pady=7)
        badge.pack_propagate(False)

        badge_image_set = False
        if HEADER_ICON_PATH:
            try:
                from PIL import Image, ImageTk
                img = Image.open(HEADER_ICON_PATH).resize((32, 32), Image.LANCZOS)
                photo = ImageTk.PhotoImage(img)
                if not hasattr(self, "_header_icons"):
                    self._header_icons = []
                self._header_icons.append(photo)
                tk.Label(badge, image=photo, bg=C4).place(relx=0.5, rely=0.5, anchor="center")
                badge_image_set = True
            except Exception as e:
                print(f"Icon load failed: {e}")

        if not badge_image_set:
            tk.Label(badge, text=APP_BADGE, bg=C4, fg="white",
                     font=(FONT_FAMILY, 8, "bold")).place(relx=0.5, rely=0.5, anchor="center")

        tf = tk.Frame(header, bg=C5)
        tf.pack(side=tk.LEFT, pady=8)
        tk.Label(tf, text=APP_TITLE, bg=C5, fg="white",
                 font=(FONT_FAMILY, 11, "bold")).pack(anchor="w")
        tk.Label(tf, text=APP_SUBTITLE, bg=C5, fg=C2,
                 font=(FONT_FAMILY, 7)).pack(anchor="w")

        if show_user and self.username:
            right = tk.Frame(header, bg=C5)
            right.pack(side=tk.RIGHT, padx=14)

            logout_btn = tk.Button(right, text="Logout",
                                   bg="white", fg=C5,
                                   font=(FONT_FAMILY, 9),
                                   relief="flat", bd=0,
                                   padx=10, pady=3,
                                   cursor="hand2",
                                   command=self.logout)
            logout_btn.pack(side=tk.RIGHT, padx=(6, 0))
            logout_btn.bind("<Enter>", lambda e: logout_btn.config(bg=C1))
            logout_btn.bind("<Leave>", lambda e: logout_btn.config(bg="white"))

            user_frame = tk.Frame(right, bg=C5)
            user_frame.pack(side=tk.RIGHT)

            avatar = tk.Frame(user_frame, bg=C3, width=24, height=24)
            avatar.pack(side=tk.LEFT, padx=(0, 6))
            avatar.pack_propagate(False)

            tk.Label(avatar, text=self.username[0].upper(), bg=C3, fg="white",
                     font=(FONT_FAMILY, 9, "bold")).place(relx=0.5, rely=0.5, anchor="center")

            tk.Label(user_frame, text=self.username,
                     bg=C5, fg="white",
                     font=(FONT_FAMILY, 10)).pack(side=tk.LEFT)

    def _label_small(self, parent, text, bg="white"):
        tk.Label(parent, text=text, bg=bg, fg=TEXT_MUTED,
                 font=(FONT_FAMILY, 8, "bold")).pack(anchor="w", pady=(14, 0))

    def _styled_entry(self, parent, show=None):
        border_frame = tk.Frame(parent, bg=C2)
        border_frame.pack(fill=tk.X, pady=(4, 0))
        inner = tk.Frame(border_frame, bg=C0)
        inner.pack(fill=tk.X, padx=1, pady=1)
        kwargs = dict(bg=C0, fg=TEXT, font=(FONT_FAMILY, 11),
                      relief="flat", bd=6, insertbackground=C5)
        if show:
            kwargs["show"] = show
        entry = tk.Entry(inner, **kwargs)
        entry.pack(fill=tk.X)

        def on_in(e):
            border_frame.config(bg=C4)
            inner.config(bg="white")
            entry.config(bg="white")
        def on_out(e):
            border_frame.config(bg=C2)
            inner.config(bg=C0)
            entry.config(bg=C0)

        entry.bind("<FocusIn>",  on_in)
        entry.bind("<FocusOut>", on_out)
        return entry

    def _btn_primary(self, parent, text, command, pady=9):
        btn = tk.Button(parent, text=text, command=command,
                        bg=C5, fg="white", font=(FONT_FAMILY, 10, "bold"),
                        relief="flat", bd=0,
                        activebackground=C4, activeforeground="white",
                        cursor="hand2", pady=pady)
        btn.pack(fill=tk.X, pady=(10, 0))
        btn.bind("<Enter>", lambda e: btn.config(bg=C4))
        btn.bind("<Leave>", lambda e: btn.config(bg=C5))
        return btn

    def _btn_ghost(self, parent, text, command, pady=7):
        border = tk.Frame(parent, bg=C2)
        border.pack(fill=tk.X, pady=(6, 0))
        btn = tk.Button(border, text=text, command=command,
                        bg="white", fg=C5, font=(FONT_FAMILY, 10),
                        relief="flat", bd=0,
                        activebackground=C0, activeforeground=C4,
                        cursor="hand2", pady=pady)
        btn.pack(fill=tk.X, padx=1, pady=1)
        btn.bind("<Enter>", lambda e: (btn.config(bg=C0, fg=C4), border.config(bg=C4)))
        btn.bind("<Leave>", lambda e: (btn.config(bg="white", fg=C5), border.config(bg=C2)))
        return btn

    def _section_card(self, parent, number, title, hint=""):
        card = tk.Frame(parent, bg="white",
                        highlightbackground=C1, highlightthickness=1)
        card.pack(fill=tk.X, pady=(0, 14))

        head = tk.Frame(card, bg="white")
        head.pack(fill=tk.X, padx=16, pady=(12, 10))

        badge = tk.Frame(head, bg=C5, width=24, height=24)
        badge.pack(side=tk.LEFT, padx=(0, 10))
        badge.pack_propagate(False)
        tk.Label(badge, text=str(number), bg=C5, fg="white",
                 font=(FONT_FAMILY, 10, "bold")).place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(head, text=title, bg="white", fg=TEXT,
                 font=(FONT_FAMILY, 12, "bold")).pack(side=tk.LEFT)

        if hint:
            tk.Label(head, text=hint, bg="white", fg=TEXT_MUTED,
                     font=(FONT_FAMILY, 8)).pack(side=tk.RIGHT)

        tk.Frame(card, bg=C1, height=1).pack(fill=tk.X)

        body = tk.Frame(card, bg="white")
        body.pack(fill=tk.X, padx=16, pady=12)
        return body

    # ══════════════════════════════════════════════════════════
    # LOGIN SCREEN
    # ══════════════════════════════════════════════════════════

    def show_login(self):
        self.clear_frame()
        self.root.geometry("700x600")
        self._make_header(self.root, show_user=False)

        center = tk.Frame(self.root, bg=C0)
        center.pack(fill=tk.BOTH, expand=True)

        card_outer = tk.Frame(center, bg=C1)
        card_outer.place(relx=0.5, rely=0.5, anchor="center")

        card = tk.Frame(card_outer, bg="white")
        card.pack(padx=2, pady=2)

        tk.Frame(card, bg=C5, width=460, height=0).pack(fill=tk.X)

        card_head = tk.Frame(card, bg=C5)
        card_head.pack(fill=tk.X)
        tk.Label(card_head, text="Welcome back",
                 bg=C5, fg="white",
                 font=(FONT_FAMILY, 18, "bold")).pack(anchor="w", padx=28, pady=(22, 2))
        tk.Label(card_head, text="Sign in to your account to continue",
                 bg=C5, fg=C2,
                 font=(FONT_FAMILY, 9)).pack(anchor="w", padx=28, pady=(0, 22))

        card_body = tk.Frame(card, bg="white")
        card_body.pack(fill=tk.X, padx=32, pady=(20, 24))

        self._label_small(card_body, "USERNAME")
        self.username_entry = self._styled_entry(card_body)
        self._label_small(card_body, "PASSWORD")
        self.password_entry = self._styled_entry(card_body, show="*")
        self._btn_primary(card_body, "Login", self.login)

        div = tk.Frame(card_body, bg="white")
        div.pack(fill=tk.X, pady=(16, 0))
        tk.Frame(div, bg=C1, height=1).pack(side=tk.LEFT, fill=tk.X, expand=True, pady=7)
        tk.Label(div, text="  no account yet?  ", bg="white",
                 fg=TEXT_MUTED, font=(FONT_FAMILY, 8)).pack(side=tk.LEFT)
        tk.Frame(div, bg=C1, height=1).pack(side=tk.LEFT, fill=tk.X, expand=True, pady=7)

        self._btn_ghost(card_body, "Create Account", self.register)

        footer = tk.Frame(card, bg=C0)
        footer.pack(fill=tk.X)
        tk.Frame(footer, bg=C1, height=1).pack(fill=tk.X)
        tk.Label(footer,
                 text="Grade Monitoring System\nFor academic tracking purposes only",
                 bg=C0, fg=TEXT_MUTED,
                 font=(FONT_FAMILY, 8), justify="center").pack(pady=12)

        self.root.bind("<Return>", lambda e: self.login())

    # ══════════════════════════════════════════════════════════
    # DASHBOARD SCREEN
    # ══════════════════════════════════════════════════════════

    def show_dashboard(self):
        self.clear_frame()
        self.main_frame = None
        self.root.geometry("1020x660")

        self._make_header(self.root, show_user=True)

        body = tk.Frame(self.root, bg=C0)
        body.pack(fill=tk.BOTH, expand=True)

        sidebar = tk.Frame(body, bg="white", width=190,
                           highlightbackground=C1, highlightthickness=1)
        sidebar.pack(side=tk.LEFT, fill=tk.Y)
        sidebar.pack_propagate(False)

        sidebar_head = tk.Frame(sidebar, bg="white")
        sidebar_head.pack(fill=tk.X, padx=12, pady=(12, 8))
        tk.Label(sidebar_head, text="SUBJECTS", bg="white", fg=TEXT_MUTED,
                 font=(FONT_FAMILY, 8, "bold")).pack(anchor="w", pady=(0, 8))

        add_subj_btn = tk.Button(sidebar_head, text="+ Add Subject",
                                 bg=C5, fg="white",
                                 font=(FONT_FAMILY, 9, "bold"),
                                 relief="flat", bd=0,
                                 cursor="hand2", pady=5,
                                 command=self.add_subject)
        add_subj_btn.pack(fill=tk.X)
        add_subj_btn.bind("<Enter>", lambda e: add_subj_btn.config(bg=C4))
        add_subj_btn.bind("<Leave>", lambda e: add_subj_btn.config(bg=C5))

        tk.Frame(sidebar, bg=C1, height=1).pack(fill=tk.X)

        self.sidebar_subject_frame = tk.Frame(sidebar, bg="white")
        self.sidebar_subject_frame.pack(fill=tk.BOTH, expand=True)

        right_panel = tk.Frame(body, bg="white", width=260,
                               highlightbackground=C1, highlightthickness=1)
        right_panel.pack(side=tk.RIGHT, fill=tk.Y)
        right_panel.pack_propagate(False)

        rp_head = tk.Frame(right_panel, bg="white")
        rp_head.pack(fill=tk.X, padx=14, pady=(12, 8))
        tk.Label(rp_head, text="GRADE RESULT", bg="white", fg=TEXT_MUTED,
                 font=(FONT_FAMILY, 8, "bold")).pack(anchor="w")
        tk.Frame(right_panel, bg=C1, height=1).pack(fill=tk.X)

        rp_body = tk.Frame(right_panel, bg="white")
        rp_body.pack(fill=tk.BOTH, expand=True, padx=14, pady=12)

        self.grade_card = tk.Frame(rp_body, bg=C5)
        self.grade_card.pack(fill=tk.X, pady=(0, 10))

        self.grade_val_label = tk.Label(self.grade_card, text="—",
                                        bg=C5, fg="white",
                                        font=(FONT_FAMILY, 36, "bold"))
        self.grade_val_label.pack(pady=(14, 0))

        tk.Label(self.grade_card, text="numeric grade",
                 bg=C5, fg=C2, font=(FONT_FAMILY, 8)).pack()

        self.grade_raw_label = tk.Label(self.grade_card, text="Raw: —",
                                        bg=C5, fg=C3,
                                        font=(FONT_FAMILY, 9))
        self.grade_raw_label.pack(pady=(4, 0))

        self.grade_status_label = tk.Label(self.grade_card, text="Not calculated",
                                           bg=C4, fg="white",
                                           font=(FONT_FAMILY, 9, "bold"),
                                           padx=12, pady=4)
        self.grade_status_label.pack(pady=(8, 14))

        self._btn_primary(rp_body, "Calculate Grade", self.calculate_grade)
        self._btn_ghost(rp_body, "↗ Project Required Score", self.show_projection)

        weight_summary_frame = tk.Frame(rp_body, bg=C0,
                                             highlightbackground=C1,
                                             highlightthickness=1)
        weight_summary_frame.pack(fill=tk.X, pady=(12, 0))
        tk.Label(weight_summary_frame, text="WEIGHT SUMMARY",
                 bg=C0, fg=TEXT_MUTED,
                 font=(FONT_FAMILY, 8, "bold")).pack(anchor="w", padx=12, pady=(10, 6))

        self.weight_total_label = tk.Label(weight_summary_frame,
                                           text="Total weight: 0%",
                                           bg=C0, fg=TEXT,
                                           font=(FONT_FAMILY, 9), anchor="w")
        self.weight_total_label.pack(fill=tk.X, padx=12)

        self.weight_remaining_label = tk.Label(weight_summary_frame,
                                           text="Remaining: 100%",
                                           bg=C0, fg=TEXT_MUTED,
                                           font=(FONT_FAMILY, 9), anchor="w")
        self.weight_remaining_label.pack(fill=tk.X, padx=12)

        self.weight_comp_label = tk.Label(weight_summary_frame,
                                           text="Component: 0",
                                           bg=C0, fg=TEXT_MUTED,
                                           font=(FONT_FAMILY, 9), anchor="w")
        self.weight_comp_label.pack(fill=tk.X, padx=12)

        bar_bg = tk.Frame(weight_summary_frame, bg=C1, height=8)
        bar_bg.pack(fill=tk.X, padx=12, pady=(8, 12))
        self.weight_bar = tk.Frame(bar_bg, bg=C4, height=8)
        self.weight_bar.place(x=0, y=0, relheight=1, relwidth=0)

        note_frame = tk.Frame(rp_body, bg=C0,
                              highlightbackground=C1, highlightthickness=1)
        note_frame.pack(fill=tk.X, pady=(10, 0))

        tk.Label(note_frame, text="NOTE",
                 bg=C0, fg=TEXT_MUTED,
                 font=(FONT_FAMILY, 7, "bold"),
                 anchor="w").pack(fill=tk.X, padx=10, pady=(8, 2))

        tk.Label(note_frame,
                 text=(
                     "For estimation only. Does not include mark "
                     "transmutation or incentive grades. Results do "
                     "not reflect final official grades."
                 ),
                 bg=C0, fg=TEXT_MUTED,
                 font=(FONT_FAMILY, 7),
                 wraplength=220, justify="left",
                 anchor="w").pack(fill=tk.X, padx=10, pady=(0, 8))

        main_outer = tk.Frame(body, bg=C0)
        main_outer.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.main_canvas = tk.Canvas(main_outer, bg=C0,
                                     highlightthickness=0, bd=0)
        scrollbar = tk.Scrollbar(main_outer, orient=tk.VERTICAL,
                                 command=self.main_canvas.yview)
        self.main_canvas.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.main_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.main_frame = tk.Frame(self.main_canvas, bg=C0)
        self.main_canvas_window = self.main_canvas.create_window(
            (0, 0), window=self.main_frame, anchor="nw"
        )

        self.main_frame.bind("<Configure>", self._on_main_frame_configure)
        self.main_canvas.bind("<Configure>", self._on_canvas_configure)
        self.main_canvas.bind_all("<MouseWheel>",
            lambda e: self.main_canvas.yview_scroll(-1 * (e.delta // 120), "units"))

        self.refresh_sidebar()

    def _on_main_frame_configure(self, event):
        self.main_canvas.configure(
            scrollregion=self.main_canvas.bbox("all")
        )

    def _on_canvas_configure(self, event):
        self.main_canvas.itemconfig(
            self.main_canvas_window, width=event.width
        )

    # ══════════════════════════════════════════════════════════
    # SIDEBAR — SUBJECT LIST
    # ══════════════════════════════════════════════════════════

    def refresh_sidebar(self):
        from subject import get_user_subjects
        for w in self.sidebar_subject_frame.winfo_children():
            w.destroy()

        subjects = get_user_subjects(self.user_id)

        if not subjects:
            tk.Label(self.sidebar_subject_frame,
                     text="No subjects yet.\nClick + Add Subject.",
                     bg="white", fg=TEXT_MUTED,
                     font=(FONT_FAMILY, 9), justify="center").pack(pady=20)
            return

        if not self.current_subject_id:
            self.current_subject_id = subjects[0][0]

        for subj in subjects:
            subj_id = subj[0]
            subj_name = subj[1]
            is_active = (subj_id == self.current_subject_id)

            row = tk.Frame(self.sidebar_subject_frame,
                           bg=C0 if is_active else "white",
                           cursor="hand2")
            row.pack(fill=tk.X)

            indicator = tk.Frame(row, bg=C5 if is_active else "white", width=3)
            indicator.pack(side=tk.LEFT, fill=tk.Y)

            lbl = tk.Label(row, text=subj_name,
                           bg=C0 if is_active else "white",
                           fg=C5 if is_active else TEXT,
                           font=(FONT_FAMILY, 10,
                                 "bold" if is_active else "normal"),
                           anchor="w", padx=10, pady=9, cursor="hand2")
            lbl.pack(side=tk.LEFT, fill=tk.X, expand=True)

            del_btn = tk.Label(row, text="✕",
                               bg=C0 if is_active else "white",
                               fg=TEXT_MUTED,
                               font=(FONT_FAMILY, 9),
                               padx=8, cursor="hand2")
            del_btn.pack(side=tk.RIGHT)

            def _on_enter(e, r=row, l=lbl, d=del_btn, active=is_active):
                if not active:
                    r.config(bg=C0);
                    l.config(bg=C0);
                    d.config(bg=C0)

            def _on_leave(e, r=row, l=lbl, d=del_btn, active=is_active):
                if not active:
                    r.config(bg="white");
                    l.config(bg="white");
                    d.config(bg="white")

            row.bind("<Enter>", _on_enter);
            row.bind("<Leave>", _on_leave)
            lbl.bind("<Enter>", _on_enter);
            lbl.bind("<Leave>", _on_leave)

            def _select(e, sid=subj_id):
                self.current_subject_id = sid
                self.refresh_sidebar()
                self.refresh_main_content()

            def _delete(e, sid=subj_id):
                self.delete_subject_by_id(sid)

            lbl.bind("<Button-1>", _select)
            row.bind("<Button-1>", _select)
            del_btn.bind("<Button-1>", _delete)

            tk.Frame(self.sidebar_subject_frame,
                     bg=C1, height=1).pack(fill=tk.X)

        self.refresh_main_content()

    # ══════════════════════════════════════════════════════════
    # MAIN CONTENT — COMPONENTS + SCORES
    # ══════════════════════════════════════════════════════════

    def refresh_main_content(self):
        from component import get_components
        from grade_logic import get_score_for_component

        if self.main_frame is None:
            return

        for w in self.main_frame.winfo_children():
            w.destroy()

        if not self.current_subject_id:
            tk.Label(self.main_frame,
                     text="Select or add a subject to get started.",
                     bg=C0, fg=TEXT_MUTED,
                     font=(FONT_FAMILY, 11)).pack(expand=True, pady=60)
            return

        wrapper = tk.Frame(self.main_frame, bg=C0)
        wrapper.pack(fill=tk.BOTH, expand=True, padx=16, pady=16)

        components = get_components(self.current_subject_id)
        total_weight = sum(c[2] for c in components) if components else 0

        comp_body = self._section_card(
            wrapper, 1, "Assessment Components",
            hint="Total weight must equal 100%"
        )

        if components:
            for idx, comp in enumerate(components):
                comp_id    = comp[0]
                comp_name  = comp[1]
                weight     = comp[2]
                total_items= comp[3]
                scores     = get_score_for_component(comp_id)

                comp_card = tk.Frame(comp_body,
                                     bg="white",
                                     highlightbackground=C1,
                                     highlightthickness=1)
                comp_card.pack(fill=tk.X, pady=(0, 10))

                comp_head = tk.Frame(comp_card, bg="white")
                comp_head.pack(fill=tk.X, padx=12, pady=(10, 6))

                tag = tk.Frame(comp_head, bg=C5, width=28, height=20)
                tag.pack(side=tk.LEFT, padx=(0, 8))
                tag.pack_propagate(False)
                tk.Label(tag, text=f"T{idx+1}", bg=C5, fg="white",
                         font=(FONT_FAMILY, 8, "bold")).place(
                             relx=0.5, rely=0.5, anchor="center")

                tk.Label(comp_head, text=comp_name, bg="white", fg=TEXT,
                         font=(FONT_FAMILY, 10, "bold")).pack(side=tk.LEFT)

                tk.Label(comp_head, text=f"{weight}%", bg="white", fg=TEXT_MUTED,
                         font=(FONT_FAMILY, 9)).pack(side=tk.LEFT)

                del_c = tk.Label(comp_head, text="✕ Remove",
                                 bg="white", fg=TEXT_MUTED,
                                 font=(FONT_FAMILY, 8), cursor="hand2")
                del_c.pack(side=tk.RIGHT, padx=4)
                del_c.bind("<Button-1>",
                           lambda e, cid=comp_id: self.delete_component_by_id(cid))
                del_c.bind("<Enter>", lambda e, l=del_c: l.config(fg=DANGER))
                del_c.bind("<Leave>", lambda e, l=del_c: l.config(fg=TEXT_MUTED))

                tk.Frame(comp_card, bg=C0, height=1).pack(fill=tk.X)

                score_row = tk.Frame(comp_card, bg="white")
                score_row.pack(fill=tk.X, padx=12, pady=8)

                tk.Label(score_row, text="Score", bg="white", fg=TEXT_MUTED,
                         font=(FONT_FAMILY, 9), width=6, anchor="w").pack(side=tk.LEFT, padx=(0, 6))

                score_var = tk.StringVar()
                score_entry = tk.Entry(score_row, textvariable=score_var,
                                       bg=C0, fg=TEXT,
                                       font=(FONT_FAMILY, 10),
                                       relief="flat", bd=4,
                                       width=7,
                                       insertbackground=C5,
                                       highlightbackground=C2,
                                       highlightthickness=1)
                score_entry.pack(side=tk.LEFT)

                tk.Label(score_row, text=f"/",
                         bg="white", fg=TEXT_MUTED,
                         font=(FONT_FAMILY, 10)).pack(side=tk.LEFT, padx=4)

                items_var = tk.StringVar()

                if total_items:
                    items_var.set(str(total_items))

                items_entry = tk.Entry(
                    score_row, textvariable=items_var,
                    bg=C0, fg=TEXT, font=(FONT_FAMILY, 10),
                    relief="flat", bd=4, width=7,
                    insertbackground=C5,
                    highlightbackground=C2, highlightthickness=1)
                items_entry.pack(side=tk.LEFT)

                tk.Label(score_row, text="total items", bg="white",
                         fg=TEXT_MUTED,
                         font=(FONT_FAMILY, 8)).pack(side=tk.LEFT, padx=(4, 8))

                add_s = tk.Button(score_row, text="+ Add",
                                  bg=C0, fg=C5,
                                  font=(FONT_FAMILY, 9, "bold"),
                                  relief="flat", bd=0,
                                  padx=8, pady=3,
                                  cursor="hand2",
                                  highlightbackground=C2,
                                  highlightthickness=1,
                                  command=lambda sv=score_var,
                                                 iv=items_var,
                                                 cid=comp_id: self._add_score_inline(sv, iv, cid))
                add_s.pack(side=tk.LEFT)
                add_s.bind("<Enter>", lambda e, b=add_s: b.config(bg=C1))
                add_s.bind("<Leave>", lambda e, b=add_s: b.config(bg=C0))


                if scores and total_items:
                    avg = sum(scores) / len(scores)
                    pct = (avg / total_items) * 100
                    earned = (pct / 100) * weight
                    summary = (f"Avg: {avg:.1f} / {total_items}  ·  "
                               f"{pct:.1f}%  ·  "
                               f"Earned: {earned:.2f}% of {weight}%")
                    summary_color = SUCCESS if pct >= 75 else WARNING if pct >= 60 else DANGER
                elif scores and not total_items:
                    summary = "Score logged - set total items to see percentage"
                    summary_color = TEXT_MUTED
                else:
                    summary = "No scores yet"
                    summary_color = TEXT_MUTED

                tk.Label(comp_card, text=summary,
                         bg="white", fg=summary_color,
                         font=(FONT_FAMILY, 8)).pack(anchor="w", padx=12, pady=(0, 10))

        else:
            tk.Label(comp_body,
                     text="No components yet. Add one below.",
                     bg="white", fg=TEXT_MUTED,
                     font=(FONT_FAMILY, 10)).pack(pady=10)

        bar_label_row = tk.Frame(comp_body, bg="white")
        bar_label_row.pack(fill=tk.X, pady=(6, 2))
        tk.Label(bar_label_row, text="Total Weight", bg="white",
                 fg=TEXT_MUTED, font=(FONT_FAMILY, 8)).pack(side=tk.LEFT)

        weight_color = (SUCCESS if total_weight == 100 else DANGER if total_weight > 100 else C4)
        weight_text  = f"{total_weight}% ✓" if total_weight == 100 else f"{total_weight}%"
        tk.Label(bar_label_row, text=weight_text, bg="white",
                 fg=weight_color,
                 font=(FONT_FAMILY, 8, "bold")).pack(side=tk.RIGHT)

        bar_bg = tk.Frame(comp_body, bg=C1, height=6)
        bar_bg.pack(fill=tk.X, pady=(0, 10))
        fill_ratio = min(total_weight / 100, 1.0)
        tk.Frame(bar_bg, bg=weight_color, height=6).place(
            x=0, y=0, relheight=1, relwidth=fill_ratio)

        add_comp_btn = tk.Button(comp_body, text="+ Add Component",
                                 bg="white", fg=TEXT_MUTED,
                                 font=(FONT_FAMILY, 9),
                                 relief="flat", bd=0,
                                 cursor="hand2", pady=8,
                                 highlightbackground=C2,
                                 highlightthickness=1,
                                 command=self.add_component)
        add_comp_btn.pack(fill=tk.X, pady=(0, 4))
        add_comp_btn.bind("<Enter>", lambda e: (
            add_comp_btn.config(fg=C4, highlightbackground=C4)))
        add_comp_btn.bind("<Leave>", lambda e: (
            add_comp_btn.config(fg=TEXT_MUTED, highlightbackground=C2)))

        self._update_weight_summary(total_weight, len(components))

    def _update_weight_summary(self, total_weight, n_components):
        remaining = max(0, 100 - total_weight)
        weight_color = (SUCCESS if total_weight == 100
                   else DANGER if total_weight > 100 else C4)
        fill_ratio = min(total_weight / 100, 1.0)

        self.weight_total_label.config(
            text=f"Total: {total_weight}%", fg= weight_color if total_weight > 0 else TEXT
        )
        self.weight_remaining_label.config(
            text=f"Remaining: {remaining}%"
        )
        self.weight_comp_label.config(
            text=f"Components: {n_components}"
        )
        self.weight_bar.place(x=0, y=0, relheight=1, relwidth=fill_ratio)
        self.weight_bar.config(bg=weight_color)

        # ══════════════════════════════════════════════════════════
        # PROJECTION WINDOW
        # ══════════════════════════════════════════════════════════

    def show_projection(self):
        """
        Opens a dedicated projection window.
        Prompts for target grade, then shows required scores per component
        using equal distribution logic.
        """
        from component import get_components, validate_weights
        from grade_logic import project_required_scores

        if not self.current_subject_id:
            messagebox.showwarning("Warning", "Select a subject first.",
                                   parent=self.root)
            return

        if not validate_weights(self.current_subject_id):
            messagebox.showwarning(
                "Warning",
                "Total component weight must equal 100%\n"
                "before projecting required scores.",
                parent=self.root)
            return

        # Ask for target grade as a percentage (e.g. 85)
        target_pct = self._ask_float(
            "Project Required Score",
            "Enter your target grade percentage (e.g. 85 for 85%):")
        if target_pct is None:
            return
        if not (0 <= target_pct <= 100):
            messagebox.showerror("Error",
                                 "Target must be between 0 and 100.",
                                 parent=self.root)
            return

        results = project_required_scores(self.current_subject_id, target_pct)
        if not results:
            messagebox.showinfo("Projection",
                                "No components found.", parent=self.root)
            return

        # ── Build projection popup window ─────────────────────
        popup = tk.Toplevel(self.root)
        popup.title("Grade Projection")
        popup.geometry("500x600")
        popup.resizable(False, False)
        popup.configure(bg=C0)
        popup.grab_set()  # Modal — focus stays here

        # Header
        ph = tk.Frame(popup, bg=C5, height=52)
        ph.pack(fill=tk.X)
        ph.pack_propagate(False)
        tk.Label(ph, text="Grade Projection",
                 bg=C5, fg="white",
                 font=(FONT_FAMILY, 13, "bold")).pack(
            side=tk.LEFT, padx=16, pady=14)

        # Target info
        target_numeric = convert_to_numeric_grade(target_pct)
        info_frame = tk.Frame(popup, bg=C0)
        info_frame.pack(fill=tk.X, padx=16, pady=(14, 0))
        tk.Label(info_frame,
                 text=f"Target: {target_pct}%  →  Numeric: {target_numeric:.2f}",
                 bg=C0, fg=TEXT,
                 font=(FONT_FAMILY, 11, "bold")).pack(anchor="w")
        tk.Label(info_frame,
                 text="Required percentage is distributed equally across unscored components.",
                 bg=C0, fg=TEXT_MUTED,
                 font=(FONT_FAMILY, 8),
                 wraplength=440, justify="left").pack(anchor="w", pady=(4, 0))

        tk.Frame(popup, bg=C1, height=1).pack(fill=tk.X, padx=16, pady=10)

        # Scrollable results
        canvas_frame = tk.Frame(popup, bg=C0)
        canvas_frame.pack(fill=tk.BOTH, expand=True, padx=16)

        proj_canvas = tk.Canvas(canvas_frame, bg=C0,
                                highlightthickness=0, bd=0)
        proj_scroll = tk.Scrollbar(canvas_frame, orient=tk.VERTICAL,
                                   command=proj_canvas.yview)
        proj_canvas.configure(yscrollcommand=proj_scroll.set)
        proj_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        proj_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        proj_inner = tk.Frame(proj_canvas, bg=C0)
        proj_win = proj_canvas.create_window(
            (0, 0), window=proj_inner, anchor="nw")

        proj_inner.bind("<Configure>", lambda e: proj_canvas.configure(
            scrollregion=proj_canvas.bbox("all")))
        proj_canvas.bind("<Configure>", lambda e: proj_canvas.itemconfig(
            proj_win, width=e.width))

        def _render_results():
            """Clear and re-render all component rows from fresh DB data."""
            from grade_logic import project_required_scores
            from database import connect_db

            for w in proj_inner.winfo_children():
                w.destroy()

            results = project_required_scores(self.current_subject_id, target_pct)

            for r in results:
                row_card = tk.Frame(proj_inner, bg="white",
                                    highlightbackground=C1, highlightthickness=1)
                row_card.pack(fill=tk.X, pady=(0, 8))

                # ── Top row: tag + name + weight + badge ──────
                top = tk.Frame(row_card, bg="white")
                top.pack(fill=tk.X, padx=12, pady=(10, 4))

                tag_f = tk.Frame(top, bg=C5 if r["has_score"] else C4,
                                 width=28, height=20)
                tag_f.pack(side=tk.LEFT, padx=(0, 8))
                tag_f.pack_propagate(False)
                tk.Label(tag_f,
                         text="✓" if r["has_score"] else "→",
                         bg=C5 if r["has_score"] else C4,
                         fg="white",
                         font=(FONT_FAMILY, 9, "bold")).place(
                    relx=0.5, rely=0.5, anchor="center")

                tk.Label(top, text=r["name"], bg="white", fg=TEXT,
                         font=(FONT_FAMILY, 10, "bold")).pack(side=tk.LEFT)
                tk.Label(top, text=f"  {r['weight']}% weight",
                         bg="white", fg=TEXT_MUTED,
                         font=(FONT_FAMILY, 9)).pack(side=tk.LEFT)

                badge_text = "Scored" if r["status"] == "done" else "Projected"
                badge_color = SUCCESS if r["status"] == "done" else C4
                tk.Label(top, text=badge_text, bg=badge_color, fg="white",
                         font=(FONT_FAMILY, 8, "bold"),
                         padx=6, pady=2).pack(side=tk.RIGHT)

                # ── Detail row ────────────────────────────────
                det = tk.Frame(row_card, bg="white")
                det.pack(fill=tk.X, padx=12)

                if r["status"] == "done":
                    # Already scored — show actual result
                    det_text = (f"Actual score: {r['actual_pct']}%  ·  "
                                f"Earned {r['earned_weight']}% "
                                f"out of {r['weight']}% weight")
                    det_color = (SUCCESS if r["actual_pct"] >= 75
                                 else WARNING if r["actual_pct"] >= 60
                    else DANGER)
                    tk.Label(det, text=det_text, bg="white", fg=det_color,
                             font=(FONT_FAMILY, 9),
                             wraplength=420, justify="left").pack(
                        anchor="w", pady=(0, 10))

                elif r["status"] == "projected":
                    # Has total_items — show required raw score
                    unachievable = r["required_pct"] > 100
                    weight_needed = round((r["required_pct"] / 100) * r["weight"], 2)
                    det_text = (
                        f"Need: {r['required_score']} / {r['total_items']}  "
                        f"({r['required_pct']}% of component)  →  "
                        f"earns {weight_needed}% of {r['weight']}% weight"
                    )
                    if unachievable:
                        det_text += "  ⚠ Target may be unachievable"
                    det_color = DANGER if unachievable else C5
                    tk.Label(det, text=det_text, bg="white", fg=det_color,
                             font=(FONT_FAMILY, 9),
                             wraplength=420, justify="left").pack(
                        anchor="w", pady=(0, 10))

                else:
                    # status == "projected_pct_only" — no total_items yet
                    # Show what weight% they need to earn, and inline input for total_items
                    unachievable = r["required_pct"] > 100
                    weight_needed = round((r["required_pct"] / 100) * r["weight"], 2)

                    # Explanation label — clear wording
                    expl = (
                        f"Need to earn {weight_needed}% out of {r['weight']}% weight  "
                        f"(i.e. score {r['required_pct']}% on this component)"
                    )
                    if unachievable:
                        expl += "  ⚠ Target may be unachievable"
                    tk.Label(det, text=expl,
                             bg="white", fg=DANGER if unachievable else C5,
                             font=(FONT_FAMILY, 9),
                             wraplength=420, justify="left").pack(anchor="w")

                    # Inline total_items entry so user can see raw score immediately
                    ti_row = tk.Frame(det, bg="white")
                    ti_row.pack(anchor="w", pady=(6, 10))

                    tk.Label(ti_row,
                             text="Enter total items to see raw score needed: ",
                             bg="white", fg=TEXT_MUTED,
                             font=(FONT_FAMILY, 8)).pack(side=tk.LEFT)

                    ti_var = tk.StringVar()
                    ti_entry = tk.Entry(ti_row, textvariable=ti_var,
                                        bg=C0, fg=TEXT,
                                        font=(FONT_FAMILY, 9),
                                        relief="flat", bd=3, width=6,
                                        highlightbackground=C2,
                                        highlightthickness=1,
                                        insertbackground=C5)
                    ti_entry.pack(side=tk.LEFT, padx=(0, 6))

                    def _set_total_items(comp_id=r["comp_id"],
                                         ti_v=ti_var):
                        """Save total_items to DB and re-render the projection."""
                        from database import connect_db as _cdb
                        val = ti_v.get().strip()
                        if not val:
                            return
                        try:
                            ti = int(val)
                            if ti <= 0:
                                raise ValueError
                        except ValueError:
                            messagebox.showerror(
                                "Error",
                                "Total items must be a positive integer.",
                                parent=popup)
                            return
                        conn = _cdb()
                        cursor = conn.cursor()
                        cursor.execute(
                            "UPDATE components SET total_items = ? "
                            "WHERE component_id = ?",
                            (ti, comp_id))
                        conn.commit()
                        conn.close()
                        # Re-render projection with new data
                        _render_results()
                        # Also refresh main dashboard
                        self.refresh_main_content()

                    set_btn = tk.Button(
                        ti_row, text="→ Show",
                        bg=C4, fg="white",
                        font=(FONT_FAMILY, 8, "bold"),
                        relief="flat", bd=0,
                        padx=6, pady=2,
                        cursor="hand2",
                        command=_set_total_items)
                    set_btn.pack(side=tk.LEFT)
                    set_btn.bind("<Enter>",
                                 lambda e, b=set_btn: b.config(bg=C5))
                    set_btn.bind("<Leave>",
                                 lambda e, b=set_btn: b.config(bg=C4))

                    # Allow Enter key inside the entry to trigger the button
                    ti_entry.bind("<Return>",
                                  lambda e, fn=_set_total_items: fn())

        # Initial render
        _render_results()

        # Close button
        tk.Frame(popup, bg=C1, height=1).pack(fill=tk.X, padx=16, pady=(8, 0))
        close_btn = tk.Button(popup, text="Close",
                              bg=C5, fg="white",
                              font=(FONT_FAMILY, 10, "bold"),
                              relief="flat", bd=0,
                              padx=20, pady=8, cursor="hand2",
                              command=popup.destroy)
        close_btn.pack(pady=12)
        close_btn.bind("<Enter>", lambda e: close_btn.config(bg=C4))
        close_btn.bind("<Leave>", lambda e: close_btn.config(bg=C5))

    # ══════════════════════════════════════════════════════════
    # SUBJECT ACTIONS
    # ══════════════════════════════════════════════════════════

    def add_subject(self):
        from subject import create_subject
        name = simpledialog.askstring("Add Subject", "Enter subject name:")
        if name and name.strip():
            create_subject(self.user_id, name.strip())
            self.refresh_sidebar()

    def delete_subject_by_id(self, subject_id):
        from database import delete_subject
        if messagebox.askyesno("Confirm", "Delete this subject and all its data?"):
            delete_subject(self.user_id, subject_id)
            if self.current_subject_id == subject_id:
                self.current_subject_id = None
            self.refresh_sidebar()

    # ══════════════════════════════════════════════════════════
    # COMPONENT ACTIONS
    # ══════════════════════════════════════════════════════════

    def add_component(self):
        from component import add_component, get_components
        if not self.current_subject_id:
            messagebox.showwarning("Warning", "Select a subject first.", parent=self.root)
            return

        name = self._ask_string("Add Component",
                                "Component name (e.g. Quizzes, Exam, Activity, etc.):"
                                )
        if not name or not name.strip():
            return

        weight = self._ask_float(
            "Add Component",
            "Weight percentage (e.g. 30 for 30%):"
        )
        if weight is None:
            return
        if weight <= 0 or weight > 100:
            messagebox.showerror("Error", "Weight must be between 1 and 100.", parent=self.root)
            return

        components = get_components(self.current_subject_id)
        current_total = sum(c[2] for c in components)
        if current_total + weight > 100:
            messagebox.showerror("Error",
                f"Adding {weight}% would exceed 100%.\n"
                f"Current total: {current_total}% | "
                f"Available: {100 - current_total}%", parent=self.root)
            return

        add_component(self.current_subject_id, name.strip(), weight, None)
        self.refresh_main_content()

    def delete_component_by_id(self, comp_id):
        from database import delete_component, delete_scores_by_component
        if messagebox.askyesno("Confirm",
                               "Delete this component and all its scores?"):
            delete_scores_by_component(comp_id)
            delete_component(self.current_subject_id, comp_id)
            self.refresh_main_content()

    # ══════════════════════════════════════════════════════════
    # SCORE ACTIONS
    # ══════════════════════════════════════════════════════════

    def _add_score_inline(self, score_var, items_var, comp_id):
        from grade_logic import add_score
        from database import connect_db

        score_str = score_var.get().strip()
        items_str = items_var.get().strip()

        if not score_str or not items_str:
            messagebox.showwarning(
                "Warning",
                "Please enter both score and total items.",
                parent=self.root)
            return

        try:
            score = float(score_str)
            total_items = int(items_str)
        except ValueError:
            messagebox.showerror("Error",
                                 "Please enter valid numbers.",
                                 parent=self.root)
            return

        if total_items <= 0:
            messagebox.showerror("Error",
                                 "Total items must be greater than 0.",
                                 parent=self.root)
            return
        if score < 0 or score > total_items:
            messagebox.showerror(
                "Error",
                f"Score must be between 0 and {total_items}.",
                parent=self.root)
            return

        # Update total_items on the component row
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE components SET total_items = ? WHERE component_id = ?",
            (total_items, comp_id))
        conn.commit()
        conn.close()

        add_score(comp_id, score)
        score_var.set("")
        self.refresh_main_content()

    # ══════════════════════════════════════════════════════════
    # GRADE ACTIONS
    # ══════════════════════════════════════════════════════════

    def calculate_grade(self):
        from grade_logic import (compute_weighted_grade, convert_to_numeric_grade,
                                 classify_performance, validate_passing_scores)
        from component import validate_weights

        if not self.current_subject_id:
            messagebox.showwarning("Warning", "Select a subject first.", parent=self.root)
            return

        passing_issues = validate_passing_scores(self.current_subject_id)
        if passing_issues:
            warnings = "\n".join(
                f"  • {i['component']}: {i['current']:.1f}% "
                f"(need 75%)"
                for i in passing_issues
            )
            messagebox.showwarning("At Risk Components",
                f"Some components are below passing threshold:\n{warnings}", parent=self.root)

        if not validate_weights(self.current_subject_id):
            messagebox.showwarning("Warning",
                "Total component weight must equal 100% before calculating.", parent=self.root)
            return

        raw_pct = compute_weighted_grade(self.current_subject_id)
        numeric  = convert_to_numeric_grade(raw_pct)
        status   = classify_performance(numeric)

        status_colors = {
            "Outstanding": SUCCESS,
            "Safe":        C4,
            "At Risk":     WARNING,
            "Critical":    DANGER
        }
        color = status_colors.get(status, C4)

        # Update right panel — numeric grade is the highlight
        self.grade_val_label.config(text=f"{numeric:.2f}")
        self.grade_raw_label.config(text=f"Raw: {raw_pct}%")
        self.grade_status_label.config(text=status, bg=color)

    # ══════════════════════════════════════════════════════════
    # AUTH
    # ══════════════════════════════════════════════════════════

    def login(self):
        from auth import login_user
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        user_id  = login_user(username, password)
        if user_id:
            self.user_id  = user_id
            self.username = username
            self.root.unbind("<Return>")
            self.show_dashboard()
        else:
            messagebox.showerror("Error", "Invalid credentials.", parent=self.root)

    def register(self):
        from auth import register_user
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        if not username or not password:
            messagebox.showerror("Error", "Fields cannot be empty.", parent=self.root)
            return
        if register_user(username, password):
            messagebox.showinfo("Success", "Account created! Please login.", parent=self.root)
            self.username_entry.delete(0, tk.END)
            self.password_entry.delete(0, tk.END)
        else:
            messagebox.showerror("Error", "Username already exists.", parent=self.root)

    def logout(self):
        if messagebox.askyesno("Logout", "Are you sure you want to logout?", parent=self.root):
            self.user_id  = None
            self.username = "user"
            self.current_subject_id = None
            self.show_login()

    def mainloop(self):
        self.root.mainloop()


# ── Entry point ────────────────────────────────────────────────
if __name__ == "__main__":
    from database import create_tables
    create_tables()
    app = GradeDashboard()
    app.mainloop()
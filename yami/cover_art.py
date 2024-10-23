"""Frame For Cover Art"""

import customtkinter as ctk


class CoverArtFrame(ctk.CTkFrame):
    """Cover Art Holder Frame"""

    def __init__(self, parent):
        super().__init__(
            parent,
        )
        self.cover_art_label = ctk.CTkLabel(
            self,
            image=None,
            text="",
            width=250,
            height=250,
            fg_color="#141414",
            corner_radius=20,
        )
        self.cover_art_label.grid(
            sticky="nsew",
        )

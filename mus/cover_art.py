import customtkinter as ctk


class CoverArtFrame(ctk.CTkFrame):
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
            corner_radius=10,
        )
        self.cover_art_label.grid(sticky="swen", padx=10)

import tkinter as tk
from tkinter import ttk, messagebox
import random
import time

class MemoryGameApp:
    def _on_game_mode_change(self, event):
        self.current_game_mode = self.game_mode_combobox.get()
        self._update_player_labels_visibility()
        self.start_new_game()

    
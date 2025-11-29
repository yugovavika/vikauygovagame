import tkinter as tk
from tkinter import ttk, messagebox
import random
import time

class MemoryGameApp:
    def _on_game_mode_change(self, event):
        self.current_game_mode = self.game_mode_combobox.get()
        self._update_player_labels_visibility()
        self.start_new_game()

    def _on_difficulty_change(self, event):
        self.current_difficulty = self.difficulty_combobox.get()
        self.start_new_game()

    def start_new_game(self):
        self.match_count = 0
        self.moves = 0
        self.game_over = False
        self.can_click = True
        self.flipped_cards = []
        self.ai_memory = {}
        self.player_scores = {"Player 1": 0, "Player 2": 0, "Computer": 0}

        if self.game_timer_id:
            self.master.after_cancel(self.game_timer_id)
        self.start_time = time.time()
        self._update_timer()

        self.moves_label.config(text="Попытки: 0")
        self.player1_score_label.config(text=f"Игрок 1: {self.player_scores['Player 1']}")
        if self.current_game_mode == "Two Players":
            self.player2_score_label.config(text=f"Игрок 2: {self.player_scores['Player 2']}")
        elif self.current_game_mode == "Player vs. AI":
            self.player2_score_label.config(text=f"Компьютер: {self.player_scores['Computer']}")

        self.current_player = "Player 1"
        self._update_current_player_display()

        self.create_game_grid()

        if self.current_game_mode == "Player vs. AI" and self.current_player == "Computer":
            self.master.after(1000, self._ai_make_move) 
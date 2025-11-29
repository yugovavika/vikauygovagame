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
    
    def on_card_click(self, card_idx):
        if self.game_over or not self.can_click:
            return

        card_info = self.cards[card_idx]

        if card_info["is_revealed"] or card_info["is_matched"]:
            return
        
        if self.current_game_mode == "Player vs. AI" and self.current_player == "Computer":
            return
        
        if len(self.flipped_cards) == 2:
            return 

        self._flip_card(card_idx, reveal=True)
        self.flipped_cards.append(card_idx)

        if self.current_game_mode == "Player vs. AI":
            symbol = card_info["symbol"]
            if symbol not in self.ai_memory:
                self.ai_memory[symbol] = []
            if card_idx not in self.ai_memory[symbol]:
                self.ai_memory[symbol].append(card_idx)

        if len(self.flipped_cards) == 2:
            self.can_click = False 
            self.moves += 1
            self.moves_label.config(text=f"Попытки: {self.moves}")
            card1_idx, card2_idx = self.flipped_cards
            card1_symbol = self.cards[card1_idx]["symbol"]
            card2_symbol = self.cards[card2_idx]["symbol"]

            if card1_symbol == card2_symbol:
                self.match_count += 1
                self.player_scores[self.current_player] += 1
                self.cards[card1_idx]["is_matched"] = True
                self.cards[card2_idx]["is_matched"] = True
                self.cards[card1_idx]["canvas"].itemconfig("border", fill=self.colors['card_matched_bg'])
                self.cards[card2_idx]["canvas"].itemconfig("border", fill=self.colors['card_matched_bg'])
                
                if self.current_game_mode == "Player vs. AI":
                    if card1_symbol in self.ai_memory:
                        self.ai_memory[card1_symbol] = [idx for idx in self.ai_memory[card1_symbol] if idx not in (card1_idx, card2_idx)]
                        if not self.ai_memory[card1_symbol]: 
                            del self.ai_memory[card1_symbol]

                self._update_scores()
                self.flipped_cards = []
                self.master.after(700, self._check_game_over_or_continue_turn) 
            else:
                self.master.after(1200, self._flip_back_and_switch_turn) 

    def _check_game_over_or_continue_turn(self):
        if self.match_count == self.total_pairs:
            self._game_over()
        else:
            self.can_click = True 
            if self.current_game_mode == "Player vs. AI" and self.current_player == "Computer":
                self.master.after(700, self._ai_make_move)
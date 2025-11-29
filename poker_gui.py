import tkinter as tk
from tkinter import messagebox, simpledialog
import poker_logic as pl
import os

class PokerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Poker Game")
        self.root.geometry("1200x800")
        self.root.configure(bg="#35654d") # Poker green background

        self.paquet = None
        self.main1 = None
        self.main2 = None
        self.current_player = 1
        self.card_images = {}
        self.back_image = None
        
        # Betting State
        self.chips = {1: 1000, 2: 1000}
        self.pot = 0
        self.current_bet = 0
        self.player_bets = {1: 0, 2: 0}
        self.phase = "START" # START, BETTING_1, EXCHANGE, BETTING_2, SHOWDOWN
        self.folded = {1: False, 2: False}
        
        # Load images
        self.load_images()

        self.setup_ui()
        self.start_game()

    def load_images(self):
        # Map French terms to English filenames
        suit_map = {
            'trèfle': 'clubs',
            'carreau': 'diamonds',
            'coeur': 'hearts',
            'pique': 'spades'
        }
        value_map = {
            'Valet': 'jack',
            'Dame': 'queen',
            'Roi': 'king',
            'As': 'ace'
        }
        
        # Load card images
        for couleur in ['trèfle', 'carreau', 'coeur', 'pique']:
            for val in ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Valet', 'Dame', 'Roi', 'As']:
                filename_val = value_map.get(val, val)
                filename_suit = suit_map[couleur]
                path = f"assets/cards/{filename_val}_of_{filename_suit}.png"
                
                if os.path.exists(path):
                    img = tk.PhotoImage(file=path)
                    # Resize (subsample)
                    img = img.subsample(2, 2) 
                    self.card_images[(val, couleur)] = img
                else:
                    print(f"Warning: Image not found {path}")

        # Load back image
        if os.path.exists("assets/cards/back.png"):
            self.back_image = tk.PhotoImage(file="assets/cards/back.png").subsample(2, 2)

    def setup_ui(self):
        # Styles
        self.bg_color = "#35654d"
        self.text_color = "white"
        self.font_title = ("Helvetica", 24, "bold")
        self.font_text = ("Helvetica", 14)
        self.font_small = ("Helvetica", 12)
        
        # Title
        self.title_label = tk.Label(self.root, text="Poker Game", font=self.font_title, bg=self.bg_color, fg=self.text_color)
        self.title_label.pack(pady=10)

        # Info Bar (Pot, Chips)
        self.info_frame = tk.Frame(self.root, bg=self.bg_color)
        self.info_frame.pack(fill="x", padx=20)
        
        self.pot_label = tk.Label(self.info_frame, text="Pot: 0", font=("Helvetica", 16, "bold"), bg=self.bg_color, fg="#ffd700")
        self.pot_label.pack(side="top", pady=5)
        
        self.p1_chips_label = tk.Label(self.info_frame, text="J1 Chips: 1000", font=self.font_small, bg=self.bg_color, fg=self.text_color)
        self.p1_chips_label.pack(side="left")
        
        self.p2_chips_label = tk.Label(self.info_frame, text="J2 Chips: 1000", font=self.font_small, bg=self.bg_color, fg=self.text_color)
        self.p2_chips_label.pack(side="right")

        # Game Area
        self.game_frame = tk.Frame(self.root, bg=self.bg_color)
        self.game_frame.pack(expand=True, fill="both")

        # Instructions
        self.instruction_label = tk.Label(self.game_frame, text="", font=self.font_text, bg=self.bg_color, fg=self.text_color)
        self.instruction_label.pack(pady=10)

        # Cards Frame
        self.cards_frame = tk.Frame(self.game_frame, bg=self.bg_color)
        self.cards_frame.pack(pady=20)

        # Controls Frame
        self.controls_frame = tk.Frame(self.root, bg=self.bg_color)
        self.controls_frame.pack(pady=20)

        # Action Buttons
        self.btn_fold = tk.Button(self.controls_frame, text="Se Coucher", command=self.action_fold, font=self.font_text, bg="#ff6b6b", width=12)
        self.btn_check_call = tk.Button(self.controls_frame, text="Parole/Suivre", command=self.action_check_call, font=self.font_text, bg="#4ecdc4", width=12)
        self.btn_raise = tk.Button(self.controls_frame, text="Relancer", command=self.action_raise, font=self.font_text, bg="#ffe66d", width=12)
        self.btn_exchange = tk.Button(self.controls_frame, text="Echanger", command=self.action_exchange, font=self.font_text, bg="white", width=12)
        
        # Result Label
        self.result_label = tk.Label(self.root, text="", font=("Helvetica", 18, "bold"), bg=self.bg_color, fg="#ffd700")
        self.result_label.pack(pady=10)

    def update_info_labels(self):
        self.pot_label.config(text=f"Pot: {self.pot}")
        self.p1_chips_label.config(text=f"J1 Chips: {self.chips[1]} (Mise: {self.player_bets[1]})")
        self.p2_chips_label.config(text=f"J2 Chips: {self.chips[2]} (Mise: {self.player_bets[2]})")

    def start_game(self):
        # Reset Round State
        self.paquet = pl.Paquet_de_cartes()
        self.paquet.battre()
        self.main1 = pl.Main("Joueur 1")
        self.main2 = pl.Main("Joueur 2")
        self.folded = {1: False, 2: False}
        self.player_bets = {1: 0, 2: 0}
        self.current_bet = 0
        self.pot = 0
        
        # Ante
        ante = 10
        if self.chips[1] < ante or self.chips[2] < ante:
            messagebox.showerror("Game Over", "Un joueur n'a plus assez de jetons !")
            return # Should handle game over properly

        self.chips[1] -= ante
        self.chips[2] -= ante
        self.pot += ante * 2
        
        self.paquet.distribuer_carte(self.main1, 5)
        self.paquet.distribuer_carte(self.main2, 5)

        self.phase = "BETTING_1"
        self.current_player = 1
        self.update_info_labels()
        self.result_label.config(text="")
        self.show_player_turn()

    def show_player_turn(self):
        # Update UI based on phase and player
        self.update_info_labels()
        
        # Clear cards
        for widget in self.cards_frame.winfo_children():
            widget.destroy()

        main = self.main1 if self.current_player == 1 else self.main2
        
        # Hide controls by default
        self.btn_fold.pack_forget()
        self.btn_check_call.pack_forget()
        self.btn_raise.pack_forget()
        self.btn_exchange.pack_forget()

        if self.phase in ["BETTING_1", "BETTING_2"]:
            self.instruction_label.config(text=f"Tour de {main.etiquette} - Mises. A suivre: {self.current_bet - self.player_bets[self.current_player]}")
            
            # Show betting controls
            self.btn_fold.pack(side="left", padx=10)
            self.btn_check_call.pack(side="left", padx=10)
            self.btn_raise.pack(side="left", padx=10)
            
            # Update button text
            to_call = self.current_bet - self.player_bets[self.current_player]
            if to_call == 0:
                self.btn_check_call.config(text="Parole")
            else:
                self.btn_check_call.config(text=f"Suivre ({to_call})")

        elif self.phase == "EXCHANGE":
            self.instruction_label.config(text=f"Tour de {main.etiquette} - Echange de cartes (Max 3)")
            self.btn_exchange.pack(side="left", padx=10)

        # Display Cards
        self.card_vars = []
        for i, carte in enumerate(main.cartes):
            var = tk.IntVar()
            self.card_vars.append(var)
            
            img = self.card_images.get((carte.get_valeur(), carte.get_couleur()))
            
            # Enable selection only in EXCHANGE phase
            state = "normal" if self.phase == "EXCHANGE" else "disabled"
            
            cb = tk.Checkbutton(self.cards_frame, image=img, variable=var, 
                                indicatoron=False, bd=4, selectcolor="#ffcccb",
                                bg="white", activebackground="white", state=state)
            cb.image = img
            cb.grid(row=0, column=i, padx=10)

    def action_fold(self):
        self.folded[self.current_player] = True
        winner = 2 if self.current_player == 1 else 1
        self.end_round_fold(winner)

    def action_check_call(self):
        to_call = self.current_bet - self.player_bets[self.current_player]
        if self.chips[self.current_player] < to_call:
            messagebox.showwarning("Attention", "Pas assez de jetons (All-in non implémenté)")
            return

        self.chips[self.current_player] -= to_call
        self.player_bets[self.current_player] += to_call
        self.pot += to_call
        
        self.next_turn()

    def action_raise(self):
        amount = simpledialog.askinteger("Relancer", "Montant de la relance :", minvalue=10, maxvalue=self.chips[self.current_player])
        if amount is None: return
        
        to_call = self.current_bet - self.player_bets[self.current_player]
        total_bet = to_call + amount
        
        if self.chips[self.current_player] < total_bet:
             messagebox.showwarning("Attention", "Pas assez de jetons")
             return

        self.chips[self.current_player] -= total_bet
        self.player_bets[self.current_player] += total_bet
        self.pot += total_bet
        self.current_bet = self.player_bets[self.current_player]
        
        # If raise, other player must respond, so we don't just advance phase, we switch player
        self.switch_player()

    def action_exchange(self):
        main = self.main1 if self.current_player == 1 else self.main2
        indices_to_change = [i for i, var in enumerate(self.card_vars) if var.get() == 1]
        
        if len(indices_to_change) > 3:
            messagebox.showwarning("Attention", "Max 3 cartes")
            return

        indices_to_change.sort(reverse=True)
        for i in indices_to_change:
            main.cartes.pop(i)
        self.paquet.distribuer_carte(main, len(indices_to_change))
        main.tri()
        
        self.next_turn()

    def switch_player(self):
        self.current_player = 2 if self.current_player == 1 else 1
        self.show_player_turn()

    def next_turn(self):
        # Logic to advance game state
        if self.phase == "BETTING_1":
            if self.player_bets[1] == self.player_bets[2] and self.player_bets[1] > 0:
                 # Betting done, move to Exchange
                 self.phase = "EXCHANGE"
                 self.current_player = 1
                 self.player_bets = {1: 0, 2: 0} # Reset bets for next round? Usually bets stay in pot.
                 self.current_bet = 0
            elif self.player_bets[1] == 0 and self.player_bets[2] == 0 and self.current_player == 2:
                 # Both checked
                 self.phase = "EXCHANGE"
                 self.current_player = 1
            else:
                self.switch_player()
                return

        elif self.phase == "EXCHANGE":
            if self.current_player == 1:
                self.switch_player()
                return
            else:
                self.phase = "BETTING_2"
                self.current_player = 1
                
        elif self.phase == "BETTING_2":
            if self.player_bets[1] == self.player_bets[2] and (self.player_bets[1] > 0 or self.current_player == 2):
                 self.show_results()
                 return
            else:
                self.switch_player()
                return
        
        self.show_player_turn()

    def end_round_fold(self, winner):
        self.chips[winner] += self.pot
        self.result_label.config(text=f"Joueur {winner} gagne le pot de {self.pot} (Adversaire couché)!")
        
        # Clear cards
        for widget in self.cards_frame.winfo_children():
            widget.destroy()
            
        self.btn_fold.pack_forget()
        self.btn_check_call.pack_forget()
        self.btn_raise.pack_forget()
        self.btn_exchange.pack_forget()
        
        tk.Button(self.controls_frame, text="Rejouer", command=self.start_game, font=self.font_text, bg="#ffd700").pack()

    def show_results(self):
        self.phase = "SHOWDOWN"
        # Clear cards frame
        for widget in self.cards_frame.winfo_children():
            widget.destroy()
            
        self.instruction_label.config(text="Résultats finaux")
        self.btn_fold.pack_forget()
        self.btn_check_call.pack_forget()
        self.btn_raise.pack_forget()
        self.btn_exchange.pack_forget()
        
        # Show Main 1
        lbl1 = tk.Label(self.cards_frame, text=f"Main Joueur 1: {self.main1.score()} points", font=("Helvetica", 12, "bold"), bg=self.bg_color, fg=self.text_color)
        lbl1.grid(row=0, column=0, columnspan=5, pady=(0, 10))
        for i, carte in enumerate(self.main1.cartes):
            img = self.card_images.get((carte.get_valeur(), carte.get_couleur()))
            lbl = tk.Label(self.cards_frame, image=img, bg="white")
            lbl.image = img
            lbl.grid(row=1, column=i, padx=5)

        # Separator
        tk.Frame(self.cards_frame, height=20, bg=self.bg_color).grid(row=2, column=0)

        # Show Main 2
        lbl2 = tk.Label(self.cards_frame, text=f"Main Joueur 2: {self.main2.score()} points", font=("Helvetica", 12, "bold"), bg=self.bg_color, fg=self.text_color)
        lbl2.grid(row=3, column=0, columnspan=5, pady=(10, 10))
        for i, carte in enumerate(self.main2.cartes):
            img = self.card_images.get((carte.get_valeur(), carte.get_couleur()))
            lbl = tk.Label(self.cards_frame, image=img, bg="white")
            lbl.image = img
            lbl.grid(row=4, column=i, padx=5)

        # Determine winner
        score1 = self.main1.score()
        score2 = self.main2.score()
        
        if score1 > score2:
            winner = 1
            text = "Le gagnant est le Joueur 1 !"
        elif score2 > score1:
            winner = 2
            text = "Le gagnant est le Joueur 2 !"
        else:
            winner = 0
            text = "C'est une égalité !!"
            
        if winner != 0:
            self.chips[winner] += self.pot
        else:
            self.chips[1] += self.pot // 2
            self.chips[2] += self.pot // 2
            
        self.result_label.config(text=text)
        self.update_info_labels()
        
        tk.Button(self.controls_frame, text="Rejouer", command=self.start_game, font=self.font_text, bg="#ffd700").pack()

if __name__ == "__main__":
    root = tk.Tk()
    app = PokerGUI(root)
    root.mainloop()

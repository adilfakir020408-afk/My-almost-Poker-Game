# 🃏 Poker Game

A graphical poker game built with Python and Tkinter, featuring a complete betting system, card exchange mechanics, and beautiful card graphics.

## 📋 Features

- **Graphical User Interface**: Clean, poker-themed GUI with green felt background
- **Real Card Images**: High-quality PNG card graphics downloaded from an online repository
- **Complete Betting System**:
  - Starting chips: 1000 per player
  - Ante system (10 chips per round)
  - Betting actions: Fold, Check/Call, Raise
  - Dynamic pot management
  - Two betting rounds (pre-exchange and post-exchange)
- **Card Exchange**: Players can exchange up to 3 cards between betting rounds
- **Hand Scoring**: Automatic detection of poker hands:
  - Pair (1 point)
  - Two Pair (2 points)
  - Three of a Kind (3 points)
  - Straight (4 points)
  - Flush (5 points)
  - Full House (6 points)
  - Four of a Kind (7 points)
  - Straight Flush (8 points)
- **Two-Player Mode**: Play against another player locally

## 🚀 Getting Started

### Prerequisites

- Python 3.x
- Tkinter (usually comes pre-installed with Python)

### Installation

1. Clone or download this repository

2. Download the card assets by running:
```bash
python download_assets.py
```

This will download all 52 card images plus the card back image into the `assets/cards/` directory.

3. Run the game:
```bash
python poker_gui.py
```

## 🎮 How to Play

### Game Flow

1. **Ante**: Each player automatically antes 10 chips to start the round
2. **Initial Deal**: Each player receives 5 cards
3. **First Betting Round**: 
   - Players take turns betting
   - Options: Fold, Check/Call, or Raise
4. **Card Exchange**: 
   - Each player can exchange up to 3 cards
   - Select cards by clicking on them, then click "Echanger"
5. **Second Betting Round**: Another round of betting
6. **Showdown**: Hands are revealed and the winner takes the pot

### Betting Actions

- **Se Coucher (Fold)**: Give up your hand and forfeit the pot
- **Parole (Check)**: Pass without betting (only when no bet to match)
- **Suivre (Call)**: Match the current bet
- **Relancer (Raise)**: Increase the bet (enter amount in dialog)

### Winning

- The player with the highest-scoring hand wins the pot
- If both players have equal scores, the pot is split
- Game continues until a player runs out of chips

## 📁 Project Structure

```
Poker Game/
├── poker_gui.py          # Main GUI application
├── poker_logic.py        # Core poker game logic (cards, hands, scoring)
├── download_assets.py    # Script to download card images
├── assets/
│   └── cards/           # Card image files (52 cards + back)
└── README.md            # This file
```

## 🎯 Code Overview

### `poker_logic.py`

Contains the core game logic:
- `Carte`: Represents a single playing card
- `Paquet_de_cartes`: Deck of 52 cards with shuffle and deal methods
- `Main`: Player's hand with scoring methods
- Hand evaluation functions: `famille()`, `quinte()`, `couleur()`, `quinteFlush()`

### `poker_gui.py`

The graphical interface:
- `PokerGUI`: Main application class
- Card image loading and display
- Betting system implementation
- Game state management (phases: START, BETTING_1, EXCHANGE, BETTING_2, SHOWDOWN)
- Player turn handling

### `download_assets.py`

Utility script that:
- Creates the `assets/cards/` directory
- Downloads card images from GitHub repository
- Handles SSL and network errors gracefully

## 🎨 Card Mapping

The game uses French card names internally but maps them to English filenames:

**Suits (Couleurs)**:
- trèfle → clubs
- carreau → diamonds
- coeur → hearts
- pique → spades

**Face Cards (Figures)**:
- Valet → jack
- Dame → queen
- Roi → king
- As → ace

## 🔧 Technical Details

- **Language**: Python 3
- **GUI Framework**: Tkinter
- **Card Images**: PNG format, subsampled 2x for display
- **Image Source**: [playing-cards-assets](https://github.com/hayeah/playing-cards-assets) repository

## 📝 Game Rules

This implementation follows simplified poker rules:
- 5-card draw poker
- Two betting rounds
- Maximum 3 cards can be exchanged
- Hand rankings from high to low: Straight Flush, Four of a Kind, Full House, Flush, Straight, Three of a Kind, Two Pair, Pair

## 🐛 Known Limitations

- All-in betting is not implemented
- No AI opponent (requires two human players)
- No save/load game state
- No hand history or statistics

## 📜 License

This is an educational project for NSI (Numérique et Sciences Informatiques).

## 🙏 Credits

- Card images from [hayeah/playing-cards-assets](https://github.com/hayeah/playing-cards-assets)
- Developed as a school project for NSI

---

**Enjoy the game! 🎰**

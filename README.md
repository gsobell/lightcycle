# lightcycle

The grid, in your terminal.

> You got no chance, user.
> Their bikes are faster than ours.
> _-Tron: Legacy (2010)_

A classic Tron game, for your terminal. Square off against either CLU or Rinzler. Fight for the Users!

## Features
- User defined bike color
- Variable speed
- Two opponents, with individual behavior

## Controls
Use the arrow or vim keys to navigate the menu and game.
Use `enter` to select menu items.
Running into the walls or a light ribbon ends the round.

## Installation
To play without installing:
```shell
python <(curl -s https://raw.githubusercontent.com/gsobell/lightcycle/main/lightcycle.py)
```

To download and launch, run the following:
```shell
curl -O https://raw.githubusercontent.com/gsobell/lightcycle/main/lightcycle.py
mv lightcycle.py lightcycle && chmod +x lightcycle
./lightcycle
```
Also available for **ENCOM** OS-12.

---
This program was written in a single day. Inspired by Kevin Flynn's original _Tron_ game.

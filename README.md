# It's so Joever
- [It's so Joever](#its-so-joever)
  - [Repository structure](#repository-structure)
    - [Assets](#assets)
    - [Src](#src)
      - [1. game.py](#1-gamepy)
      - [2. gui.py](#2-guipy)
      - [3. dbHandler.py](#3-dbhandlerpy)
      - [4. login.py](#4-loginpy)
      - [5. leaderboard.py](#5-leaderboardpy)
      - [6. common.py](#6-commonpy)
  - [Setup and start](#setup-and-start)
  - [Gameplay](#gameplay)
    - [Main mechanics](#main-mechanics)
    - [Powerup mechanics](#powerup-mechanics)
    - [Crises](#crises)
  - [Problem Statement](#problem-statement)
  - [Background Story](#background-story)
  - [Scenario](#scenario)
  - [Python Concepts](#python-concepts)
  - [Key Features](#key-features)
  - [References](#references)
  - [Disclaimers](#disclaimers)

## Repository structure

### Assets

### Src
#### 1. game.py
#### 2. gui.py
#### 3. dbHandler.py
#### 4. login.py
#### 5. leaderboard.py
#### 6. common.py


## Setup and start
Environment setup: in your desired environment, enter
`pip install -r requirements.txt`
into the terminal

To start the game on Windows (in your desired environment): `py <path>/<to>/<game>/game.py`

To start the game on anything else (Mac/Linux): `python3 <path>/<to>/<game>/game.py`

---

## Gameplay
### Main mechanics
Click the coin to print more coins!!

The game's concept is inspired by Cookie Clicker. The main point of the game is to print as many SUTD coins as possible by clicking, all within a fixed duration. However, several "crises" may emerge, causing printing to halt unless they are addressed appropriately.

### Powerup mechanics
1. Anyquadratic Printer
2. Bamboo printer
3. Douyin Ion Thrusters
4. November

### Crises
1. No filament
2. No printer bed
3. Error code HMS_05000-100-003-0005
   
---

## Problem Statement
The maintenance of 3D printers poses significant challenges due to the complexities of mechanical and electrical components, the lack of standardization across models, and the need for regular calibration. As a student at the Singapore University of Technology and Design (SUTD), we often encounter issues in troubleshooting. Additionally, besides the technical situations, we also face interruptions from 3rd parties. As a result, there is a reduction in print quality, downtime, and frustration at times. 

As SUTD students well-versed in manoeuvring such intricate challenges, we are on a mission to better the world with our knowledge.

---

## Background Story
This game was created for SUTDents in general, especially for students who have little to no experience with 3D printing. Due to the importance of 3D printing in our curriculum, students need to know the potential problems they may encounter when printing. As such, in our game, we have incorporated these problems that may arise and the appropriate solutions to remedy them. A game with occasional curveballs will equip SUTDents with the fundamental know-how to better navigate such a piece of complex machinery.

---

## Scenario
The intended demographic is SUTDents in general however it is not necessarily limited to SUTD. Given the popularity of 3D printing nowadays, anyone worldwide with some knowledge of 3D printing and access to 3D printers can engage in our game. Having played our game, players can have a rough idea of the potential problems they may encounter and they will be equipped with the basic capability to tinker with 3D printers in the future.

---

## Python Concepts
1. Tkinter ([gui.py](#2-guipy))
2. SQLite ([dbHandler.py](#3-dbhandlerpy))
3. Classes, OOP ([game.py](#1-gamepy))
4. Functions
5. If/ Else statements
6. Exception handling
7. Callback functions 
8. Procedural programming ([dbHandler.py](#3-dbhandlerpy))

---

## Key Features
1. Gamification of an educational game.
2. SQLite, a light-weight database
3. Tkinter - to construct GUIs
4. Leaderboard
5. Relatable for SUTD students

## References
Ian Bogost. (2010). Cow Clicker [Facebook].

Julien Theinnot. (2021). Cookie Clicker [Steam]. Playsaurus.

---

## Disclaimers
Any resemblance to any living or non-living persons is purely coincidental.

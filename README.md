# COMPUTER PROGRAMMING, ALGORITHMS AND DATA STRUCTURES - MOD 1  
## CANNON GAME  
### FINAL EXAM PROJECT 2023/2024

## General Information
The aim of this project was the development of a video game, based on artillery retro games. It was created using Python and the Kivy library. The game runs with two files, `CannonGame.py` and `cannon.kv`.

### The Kivy Framework
The `cannon.kv` file was mainly used to create the GUI of the game, allowing the player to interact with different buttons. A box layout was used to organize the widgets. Sliders were used to adjust the angle and muzzle velocity of the cannon, as these controls allowed a wider range of values. Since the game is designed to be played with the mouse, the `TextInput` widget was avoided to prevent keyboard usage. For the menu aspects like pop-ups, labels, buttons, and text input, I mainly used `kivy.uix`. I also utilized `kivy.properties` for widget values and `kivy.graphics` for designing bullets and obstacles. `kivy.clock` scheduled regular intervals to animate the game, and `kivy.core.audio` was used for background music and sound effects.

### General Structure of the Game
The game is composed of multiple levels. To pass a level, the player must hit the target on the right side of the screen. There is no limit on the number of shots, and the objective is to finish all levels using as few shots as possible. Initially, I planned to limit the number of shots per level, but I changed this to make the game more replayable. The hall of fame lists players who finished the game, ranked by the number of shots used.

### The `CannonGame` Class
This is the main class from which the whole game is built. It contains initial values and primary functions. The `__init__` function sets up variables and level design, drawing the background and obstacles first. The projectiles are drawn using the `canvas` object after the `draw_projectile` function is called by `start_shot`, which is bound to the Fire button.

After the initial velocity is calculated, the environment and projectile position are updated every 1/20 of a second, with the update function called by `kivy.clock`. The projectile’s position is affected by gravity, and collision checks are performed:
- **Target collision**: Advances the game to the next level.
- **Rock collision**: The projectile stops, and the obstacle is removed.
- **Perpetio collision**: The projectile stops, but the obstacle remains.
- **Bulletproof mirror**: The projectile is reflected if it’s a laser; otherwise, it stops.
- **Floor collision**: The projectile is destroyed.

After the last round, a popup shows the player's score and prompts for a name to be stored in the hall of fame. The game then resets, allowing the player to try again and beat the high score.

### The Projectiles
There are three types of projectiles: bullet, bombshell, and laser, with distinct behaviors:
- **Bullet**: Affected by gravity, follows a parabolic trajectory, and has a high maximum velocity. It doesn’t get destroyed after hitting an obstacle.
- **Bombshell**: Affected by gravity, slow, explodes on impact, penetrating the obstacle it hits, and is then destroyed.
- **Laser**: Not affected by gravity, follows a straight-line trajectory, and penetrates obstacles, including those behind the first one.

The laser was modified from its original design to make implementation simpler, with `LASER_IMPULSE` representing the laser’s length. Collision detection for the projectiles involves calculating distances using the Euclidean formula. The laser uniquely interacts with the mirror, being the only projectile that gets reflected. The biggest challenge was updating the drawing of the laser post-reflection to match its new angle.

### Constants and Additional Libraries Used
All constants are listed at the beginning of the code. I made minor changes to `BULLET_MASS` and `BOMB_MASS` and added a new gravity constant. I adjusted the gravity multiplier to 25 for noticeable gameplay effects. In addition to the Kivy library, I used `math` for angle and distance calculations and `json` to store game information in `save_game.json`.

### Game Assets
The assets folder contains all textures and sounds used in the game:
- Sky and floor textures were created by Erik Sandberg in a YouTube course on recreating the Flappy Bird game [1].
- Cannon and target images were pixel art from Freepik [3].
- Rock and perpetio obstacle textures were created using Pixilart [4], inspired by Minecraft [5].
- Background music was a western track downloaded from Pixabay [6].
- The target hit sound effect was sourced from Soundsnap [7].

### Possible Improvements
Future improvements include adding more obstacles for greater level variety. Bullet physics could be refined to make muzzle velocity more significant and allow bullets to bounce after colliding with obstacles. Additionally, the rock obstacle could be affected by gravity and break into fragments after being destroyed.

---

## References
[1] "Python Game Development with Kivy: Infinite Scrolling Background"  
   [Dirk Sandberg's 2DKivyGame](https://github.com/Dirk-Sandberg/2DKivyGame).  
[2] "Flappy Bird" - [Wikipedia](https://en.wikipedia.org/wiki/Flappy_Bird).  
[3] "Freepik" - [Freepik Website](https://www.freepik.com/).  
[4] "Pixilart" - [Pixilart Website](https://www.pixilart.com/).  
[5] "Minecraft" - [Wikipedia](https://en.wikipedia.org/wiki/Minecraft).  
[6] "Pixabay" - [Pixabay Website](https://pixabay.com/).  
[7] "Soundsnap" - [Soundsnap Website](https://www.soundsnap.com/).

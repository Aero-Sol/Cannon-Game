from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import NumericProperty, StringProperty, BooleanProperty
from kivy.clock import Clock
from kivy.graphics import Color, Ellipse, Line, Rectangle
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
import math
import json

# Constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 750
FPS = 20
BULLET_RADIUS = SCREEN_WIDTH / 100
BOMB_RADIUS = SCREEN_WIDTH / 50
LASER_DIST = SCREEN_WIDTH / 100
GRAVITY = 98

# Projectile constants
BULLET_MASS = SCREEN_WIDTH / 2
BOMB_MASS = SCREEN_WIDTH / 3
BULLET_MAX_VEL = BULLET_MASS
BOMB_MAX_VEL = BOMB_MASS
LASER_VEL = SCREEN_WIDTH / 1.5
BULLET_GRAVITY = True
BOMB_GRAVITY = True
LASER_GRAVITY = False
BOMB_DRILL = SCREEN_WIDTH / 20
LASER_IMPULSE = SCREEN_WIDTH / 20


class Obstacle:
    """Base class for game obstacles."""
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.canvas_instructions = []
        self.canvas = None

    def draw(self, canvas):
        """Draw the obstacle on the canvas."""
        self.canvas = canvas  # store canvas references

    def clear_drawing(self):
        """Clear the obstacle's drawing from the canvas."""
        if self.canvas and self.canvas_instructions:
            for instruction in self.canvas_instructions:
                self.canvas.remove(instruction)
            self.canvas_instructions = []


class Rock(Obstacle):
    """Rock obstacle class."""
    def draw(self, canvas):
        """Draw the rock obstacle as a rectangle."""
        super().draw(canvas)  # Call the parent class's draw method
        with canvas:
            rect = Rectangle(source='assets/rock.png', pos=(self.x, self.y), size=(self.width, self.height))
            self.canvas_instructions.append(rect)


class BulletproofMirror(Obstacle):
    """BulletproofMirror obstacle class."""
    def draw(self, canvas):
        """Draw the bulletproof mirror obstacle as a line."""
        super().draw(canvas)  # Call the parent class's draw method
        with canvas:
            Color(1, 0, 1)
            line = Line(points=[self.x, self.y, self.x + self.width, self.y])
            self.canvas_instructions.append(line)


class Perpetio(Obstacle):
    """Perpetio obstacle class."""
    def draw(self, canvas):
        """Draw the Perpetio obstacle as a rectangle."""
        super().draw(canvas)  # Call the parent class's draw method
        with canvas:
            rect = Rectangle(source='assets/perpetio.png', pos=(self.x, self.y), size=(self.width, self.height))
            self.canvas_instructions.append(rect)


class Floor(Obstacle):
    """Floor obstacle class."""
    def draw(self, canvas):
        """Draw the floor obstacle as a rectangle."""
        super().draw(canvas)  # Call the parent class's draw method
        with canvas:
            rect = Rectangle(source='assets/floor.png', pos=(self.x, self.y), size=(self.width, self.height))
            self.canvas_instructions.append(rect)


class CannonGame(BoxLayout):
    """Main class representing the Cannon game."""
    angle = NumericProperty(45)
    velocity = NumericProperty(500)
    type_of_shot = StringProperty("Bullet")
    score = NumericProperty(0)
    shots = NumericProperty(0)
    shot_fired = BooleanProperty(False)
    round_number = NumericProperty(1)
    level = NumericProperty(1)

    obstacles = []

    hall_of_fame = []  # List to store scores

    def add_to_hall_of_fame(self, player_name):
        """Add player's score to the hall of fame."""
        self.hall_of_fame.append((player_name, self.shots))
        self.hall_of_fame.sort(key=lambda x: x[1])  # Sort scores in descending order

    def __init__(self, **kwargs):
        """Initialize the game."""
        super(CannonGame, self).__init__(**kwargs)
        self.projectile_instructions = []
        self.target_x = SCREEN_WIDTH - 200
        self.target_y = 200
        self.target_width = 150
        self.target_height = 150
        self.target_radius = self.target_width / 2
        self.projectile = None
        self.projectile_x = 0
        self.projectile_y = 0
        self.projectile_velocity_x = 0
        self.projectile_velocity_y = 0
        self.bombshell_penetrated = False
        self.init_graphics()
        self.setup_level()
        Clock.schedule_interval(self.update, 1.0 / FPS)

    def init_graphics(self):
        """Initialize the graphics."""
        with self.canvas.before:
            # Draw the background
            self.sky = Rectangle(pos=(0, 0), size=(SCREEN_WIDTH, SCREEN_HEIGHT), source='assets/sky.png')
        with self.canvas:
            # Draw the cannon
            self.cannon = Rectangle(pos=(0, 80), size=(100, 100), source='assets/cannon.png')
            # Draw the target
            self.target = Ellipse(pos=(self.target_x, self.target_y), size=(self.target_width, self.target_height), source='assets/target.png')

    def clear_obstacles(self):
        for obstacle in self.obstacles:
            obstacle.clear_drawing()
        self.obstacles = []

    def reset_game(self):
        """Reset the game to its initial state."""
        self.round_number = 1
        self.level = 1
        self.setup_level()
        self.reset()

    def setup_level(self):
        """Setup the game level."""
        self.clear_obstacles()
        self.obstacles = [Floor(x=0, y=30, width=SCREEN_WIDTH, height=50)]  # The floor is always present as an obstacle
        if self.level == 1:
            pass
        elif self.level == 2:
            self.obstacles.append(Perpetio(x=400, y=80, width=100, height=300))
        elif self.level == 3:
            self.obstacles.append(Rock(x=400, y=230, width=10, height=200))
            self.obstacles.append(Rock(x=420, y=230, width=30, height=150))
            self.obstacles.append(Rock(x=440, y=380, width=20, height=40))
            self.obstacles.append(Rock(x=500, y=230, width=20, height=40))
            self.obstacles.append(Perpetio(x=400, y=80, width=150, height=150))
        elif self.level == 4:
            self.obstacles.append(Perpetio(x=400, y=80, width=100, height=300))
            self.obstacles.append(BulletproofMirror(x=300, y=600, width=400, height=20))
        elif self.level == 5:
            self.obstacles.append(BulletproofMirror(x=100, y=600, width=300, height=20))
            self.obstacles.append(BulletproofMirror(x=300, y=100, width=300, height=20))
            self.obstacles.append(BulletproofMirror(x=550, y=600, width=300, height=20))
            self.obstacles.append(Perpetio(x=450, y=350, width=50, height=300))
            self.obstacles.append(Perpetio(x=250, y=80, width=50, height=250))
            self.obstacles.append(Perpetio(x=680, y=80, width=50, height=250))
        elif self.level == 6:
            self.obstacles.append(Perpetio(x=0, y=550, width=SCREEN_WIDTH, height=50))
            self.obstacles.append(Perpetio(x=700, y=80, width=50, height=300))

        self.draw_obstacles()

    def draw_obstacles(self):
        """Draw the obstacles."""
        for obstacle in self.obstacles:
            obstacle.draw(self.canvas)
    
    def clear_projectiles(self):
        """Clear all projectiles from the canvas."""
        for instruction in self.projectile_instructions:
            self.canvas.remove(instruction)
        self.projectile_instructions = []

    def draw_projectile(self):
        """Draw the projectile."""
        self.clear_projectiles() # Clear existing projectiles

        with self.canvas:
            if self.type_of_shot == "Bullet":
                Color(0, 0, 0)
                self.projectile = Ellipse(pos=(self.projectile_x, self.projectile_y), size=(10, 10))
                self.projectile_instructions.append(self.projectile)
            elif self.type_of_shot == "Bombshell":
                Color(0, 0, 0)
                self.projectile = Ellipse(pos=(self.projectile_x, self.projectile_y), size=(20, 20))
                self.projectile_instructions.append(self.projectile)
            elif self.type_of_shot == "Laser":
                Color(1, 0, 0)
                angle = math.atan2(self.projectile_velocity_y, self.projectile_velocity_x)
                end_x = self.projectile_x + LASER_IMPULSE * math.cos(angle)
                end_y = self.projectile_y + LASER_IMPULSE * math.sin(angle)
                self.projectile = Line(points=[self.projectile_x, self.projectile_y, end_x, end_y], width=2)
                self.projectile_instructions.append(self.projectile)
            Color(1, 1, 1) # Reset color

    def start_shot(self):
        """Start a shot."""
        self.shot_fired = True
        self.projectile_x = 100
        self.projectile_y = 100
        self.shots += 1
        if self.type_of_shot == "Laser":
            self.velocity = LASER_VEL
        self.calculate_initial_velocity()
        self.draw_projectile()

    def calculate_initial_velocity(self):
        """Calculate initial velocity of the projectile."""
        rad = math.radians(self.angle)
        self.projectile_velocity_x = self.velocity * math.cos(rad)
        self.projectile_velocity_y = self.velocity * math.sin(rad)

    def update(self, dt):
        if not self.shot_fired:
            return

        if self.type_of_shot != "Laser":
            if self.type_of_shot == "Bullet" and BULLET_GRAVITY:
                self.projectile_velocity_y -= GRAVITY * dt
            elif self.type_of_shot == "Bombshell" and BOMB_GRAVITY:
                self.projectile_velocity_y -= GRAVITY * dt

            self.projectile_x += self.projectile_velocity_x * dt
            self.projectile_y += self.projectile_velocity_y * dt
        else:
            self.projectile_x += self.projectile_velocity_x * dt
            self.projectile_y += self.projectile_velocity_y * dt

        if self.projectile_x > SCREEN_WIDTH or self.projectile_y > SCREEN_HEIGHT:
            self.reset()

        self.draw_projectile()
        self.check_collision()

    def check_collision(self):
        """Check for collisions between the projectile and the target or obstacles."""
        if self.type_of_shot == "Bullet":
            radius = BULLET_RADIUS
        elif self.type_of_shot == "Bombshell":
            radius = BOMB_RADIUS 
        elif self.type_of_shot == "Laser":
            radius = LASER_DIST
        else:
            radius = 0  # Default case

        # Check collision with the target
        distance_to_target = math.sqrt((self.projectile_x - (self.target_x + self.target_radius)) ** 2 +
                                       (self.projectile_y - (self.target_y + self.target_radius)) ** 2)
        if distance_to_target < radius + 100:  # Add extra margin for collision detection
            self.end_round()
            return

        # Check collision with obstacles
        for obstacle in self.obstacles:
            if self.collides_with_obstacle(obstacle, radius):
                self.projectile_collision(obstacle)
                return

    def collides_with_obstacle(self, obstacle, radius):
        closest_x = max(obstacle.x, min(self.projectile_x, obstacle.x + obstacle.width))
        closest_y = max(obstacle.y, min(self.projectile_y, obstacle.y + obstacle.height))
        distance = math.sqrt((self.projectile_x - closest_x) ** 2 + (self.projectile_y - closest_y) ** 2)
        return distance < radius

    def projectile_collision(self, obstacle):
        """Handle collision of the projectile with obstacles."""
        if isinstance(obstacle, Rock):
            if self.type_of_shot in ["Bombshell", "Laser"]:
                self.bombshell_penetrated = False
                self.penetrate_obstacle(obstacle)
                Clock.schedule_once(self.remove_bombshell, 0.1)
            self.projectile_velocity_x = 0
            self.projectile_velocity_y = 0
            obstacle.clear_drawing()  # remove the drawing of the rock
            self.obstacles.remove(obstacle)
        elif isinstance(obstacle, BulletproofMirror):
            if self.type_of_shot == "Laser":
                # Calculate the angle of incidence
                incident_angle = math.atan2(self.projectile_velocity_y, self.projectile_velocity_x)
                mirror_angle = 0
                # Calculate the angle of reflection
                reflection_angle = 2 * mirror_angle - incident_angle
            
                # Update the velocity components for the reflected laser
                speed = math.sqrt(self.projectile_velocity_x**2 + self.projectile_velocity_y**2)
                self.projectile_velocity_x = speed * math.cos(reflection_angle)
                self.projectile_velocity_y = speed * math.sin(reflection_angle)
            
                # Update the projectile's position to avoid getting stuck in the mirror
                self.projectile_y = obstacle.y + 1  # Move it slightly above the mirror
            else:
                self.projectile_velocity_x = 0
                self.projectile_velocity_y = 0
        elif isinstance(obstacle, Perpetio):
            if self.type_of_shot in ["Bombshell", "Laser"]:
                self.bombshell_penetrated = False
                self.penetrate_obstacle(obstacle)
                Clock.schedule_once(self.remove_bombshell, 0.1) # Schedule the removal of the bombshell after a short delay
            # Do nothing, as Perpetio cannot be destroyed
            self.projectile_velocity_x = 0
            self.projectile_velocity_y = 0
        elif isinstance(obstacle, Floor):
            self.reset()

    def remove_bombshell(self, dt):
        if not self.bombshell_penetrated:
            self.clear_projectiles()
            self.shot_fired = False
            self.bombshell_penetrated = True

    def penetrate_obstacle(self, obstacle):
        rad = math.atan2(self.projectile_velocity_y, self.projectile_velocity_x)
        if self.type_of_shot == "Bombshell":
            penetration_x = self.projectile_x + BOMB_DRILL * math.cos(rad)
            penetration_y = self.projectile_y + BOMB_DRILL * math.sin(rad)
            penetration_radius = BOMB_RADIUS
        elif self.type_of_shot == "Laser":
            penetration_x = self.projectile_x + LASER_IMPULSE * math.cos(rad)
            penetration_y = self.projectile_y + LASER_IMPULSE * math.sin(rad)
            penetration_radius = LASER_DIST

        for obs in self.obstacles:
            if obs != obstacle:  # Skip the initial obstacle for penetration
                distance_to_obstacle = math.sqrt((penetration_x - obs.x) ** 2 +
                                                (penetration_y - obs.y) ** 2)
                if distance_to_obstacle < penetration_radius:
                    obs.clear_drawing()
                    self.obstacles.remove(obs)
        
        if self.type_of_shot == "Bombshell":
            self.projectile_x = penetration_x
            self.projectile_y = penetration_y
        else:
            self.projectile_x = penetration_x
            self.projectile_y = penetration_y

        if self.projectile_velocity_x == 0 and self.projectile_velocity_y == 0:
            self.reset()

    def reset(self):
        """Reset the game."""
        self.projectile_x = 0
        self.projectile_y = 0
        self.shot_fired = False
        self.angle = 45
        self.velocity = 500
        self.clear_projectiles()
        self.draw_projectile()
        self.draw_obstacles()

    def end_round(self):
        """End the round."""
        self.clear_obstacles()

        if self.round_number == 6:
            popup_content = EndGameContent(shots=self.shots, game_instance=self)
            popup = Popup(title=f'Congratulations! You are a faggot!!!!! {self.shots}',
                          content=popup_content,
                          size_hint=(None, None), size=(400, 200))
            popup_content.popup = popup
            popup.open()

            # Prompt player for name and add score to hall of fame
            popup_content.prompt_for_name()
            self.reset_game()
        else:
            # Advance to the next level
            self.level += 1
            self.setup_level()
            print(f"Level advanced to {self.level}")
            self.round_number += 1
            self.reset()

    def save_game(self):
        """Save the game state to a JSON file."""
        game_data = {
            "angle": self.angle,
            "velocity": self.velocity,
            "type_of_shot": self.type_of_shot,
            "shots": self.shots,
            "round_number": self.round_number,
            "level": self.level
        }
        with open("save_game.json", "w") as file:
            json.dump(game_data, file)
        print("Game Saved!")

    def load_game(self):
        try:
            with open("save_game.json", "r") as file:
                game_data = json.load(file)
                self.angle = game_data["angle"]
                self.velocity = game_data["velocity"]
                self.type_of_shot = game_data["type_of_shot"]
                self.shots = game_data["shots"]
                self.round_number = game_data["round_number"]
                self.level = game_data["level"]
                self.setup_level()
                print("Game Loaded!")
        except FileNotFoundError:
            print("No saved game found!")

    def show_hall_of_fame(self):
        """Show the hall of fame."""
        popup = HallOfFamePopup(title='Hall of Fame', hall_of_fame=self.hall_of_fame,
                                size_hint=(None, None), size=(400, 400))
        popup.open()

    def show_help(self):
        """Show the help popup."""
        popup = Popup(title='Help',
                      content=HelpContent(),
                      size_hint=(None, None), size=(700, 450))
        popup.open()


class EndGameContent(BoxLayout):
    """Content for the end of round popup."""
    score = NumericProperty(0)
    shots = NumericProperty(0)
    game_instance = None
    popup = None

    def __init__(self, shots, game_instance, **kwargs):
        """Initialize end of round content."""
        super(EndGameContent, self).__init__(**kwargs)
        self.shots = shots
        self.game_instance = game_instance

    def prompt_for_name(self):
        """Prompt the player for their name."""
        self.clear_widgets()  # Clear existing widgets
        name_input = TextInput(hint_text='Enter your name', multiline=False)
        submit_button = Button(text='Submit', size_hint_y=None, height=30)
        submit_button.bind(on_press=lambda instance: self.submit_score(name_input.text))
        self.add_widget(name_input)
        self.add_widget(submit_button)

    def submit_score(self, player_name):
        """Submit the player's score."""
        self.game_instance.add_to_hall_of_fame(player_name)
        self.game_instance.shots = 0  # Reset shots counter
        self.popup.dismiss()


class HallOfFamePopup(Popup):
    """Popup for the hall of fame."""
    def __init__(self, hall_of_fame, **kwargs):
        """Initialize the hall of fame popup."""
        super(HallOfFamePopup, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')
        for idx, (name, shots) in enumerate(hall_of_fame, 1):
            label = Label(text=f'{idx}. {name}: {shots}')
            layout.add_widget(label)
        self.content = layout


class HallOfFameContent(BoxLayout):
    """Content for the hall of fame."""
    def close_popup(self):
        """Close the hall of fame popup."""
        self.parent.dismiss()


class HelpContent(BoxLayout):
    """Content for the help popup."""
    def close_popup(self):
        """Close the help popup."""
        self.parent.dismiss()


class CannonApp(App):
    """Main application class."""
    def build(self):
        """Build the application."""
        return CannonGame()


if __name__ == '__main__':
    CannonApp().run()

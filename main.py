# Import needed modules
import arcade
from PIL import Image

# Load fonts
arcade.load_font('fonts/SFPixelate-Bold.ttf')
arcade.load_font('fonts/SFPixelateShaded-Bold.ttf')

# Basic
level = 1
level_data = {
    1: {'offset': 1600, 'lowest': -40, 'obs': 2, 'k': 3}
}


class Homepage(arcade.View):
    def __init__(self):
        # Run Setup function with all setup in it
        super().__init__()

        # Early setup for variables.
        self.cursor_visible = None
        self.cursor_visible = None
        self.mouse_y = None
        self.mouse_x = None
        self.cursor = None
        self.screen_switch = None
        self.screen_to_switch = None
        self.screen_to_switch = None
        self.switch_in = None
        self.black = None
        self.buttons = None
        self.camera = None

        # Run setup
        self.setup()

    def on_show_view(self):
        self.setup()
        self.adjust_camera()

    def setup(self):
        # Set bg color to dark white
        arcade.set_background_color((0, 0, 0, 1))

        # Camera
        self.camera = arcade.Camera2D(projection=arcade.XYWH(0.0, 0.0, 800.0, 600.0))

        # Hide mouse
        self.window.set_mouse_visible(False)

        # Window Switch
        self.black = arcade.Sprite('assets/GLOBAL/black.png')
        self.black.position = WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2
        self.screen_switch = True
        self.switch_in = True
        self.screen_to_switch = None

        # Load custom cursor
        self.cursor = arcade.Sprite('assets/GLOBAL/cursor.png')
        self.cursor.scale = 4

        # Setup mouse tracking variables
        self.mouse_x = -32
        self.mouse_y = -32
        self.cursor_visible = True

        # Load button
        temp = arcade.Sprite('assets/homepage/button.png')
        temp.scale = 0.3
        temp.position = WINDOW_WIDTH // 2, 300
        self.buttons = arcade.SpriteList()
        self.buttons.append(temp)

    def on_draw(self):
        with self.camera.activate():
            self.window.clear()
            self.buttons.draw(pixelated=True)
            if self.cursor_visible:
                arcade.draw_sprite(self.cursor, pixelated=True)
            arcade.draw_sprite(self.black)

    def on_update(self, delta_time):
        x_, y_, _ = self.camera.unproject((self.mouse_x, self.mouse_y))
        if self.screen_switch:
            if self.switch_in:
                self.black.alpha = max(self.black.alpha - 8, 0)
            else:
                self.black.alpha = min(self.black.alpha + 8, 255)
            if self.black.alpha < 5 and self.switch_in:
                self.screen_switch = False
                self.switch_in = False
                self.black.alpha = 0
            if self.black.alpha > 250 and not self.switch_in:
                self.screen_switch = False
                self.black.alpha = 255
                if self.screen_to_switch == 'level_selection':
                    self.window.show_view(level_selection)

        # Move cursor to mouse position
        self.cursor.position = x_ + 16, y_ - 16

    def on_mouse_press(self, x, y, button, modifiers):
        x_, y_, _ = self.camera.unproject((x, y))
        if not self.screen_switch:
            if arcade.get_sprites_at_point((x_, y_), self.buttons):
                self.screen_switch = True
                self.screen_to_switch = 'level_selection'
            # if arcade.get_sprites_at_point((x_, y_), self.exit_button):
            #     arcade.exit()

    def on_resize(self, width, height):
        self.adjust_camera()

    def adjust_camera(self):
        height = self.window.height
        width = self.window.width
        if height / 3.0 < width / 4.0:
            h = height
            w = 4.0 / 3.0 * height
        else:
            h = 3.0 / 4.0 * width
            w = width

        self.camera.viewport = arcade.XYWH(width / 2.0, height / 2.0, w, h)
        self.camera.position = self.camera.width / 2.0, self.camera.height / 2.0

    def on_mouse_motion(self, x, y, dx, dy):
        self.mouse_x = x
        self.mouse_y = y

    def on_mouse_enter(self, x, y):
        self.cursor_visible = True
        self.window.set_mouse_visible(False)
        self.mouse_x = x
        self.mouse_y = y

    def on_mouse_leave(self, x, y):
        self.cursor_visible = False
        self.window.set_mouse_visible(True)


class LevelSelection(arcade.View):
    def __init__(self):
        # Run Setup function with all setup in it
        super().__init__()

        # Early setup for variables.
        self.cursor_visible = None
        self.cursor_visible = None
        self.mouse_y = None
        self.mouse_x = None
        self.cursor = None
        self.screen_switch = None
        self.screen_to_switch = None
        self.screen_to_switch = None
        self.switch_in = None
        self.black = None
        self.camera = None

    def on_show_view(self):
        self.setup()
        self.adjust_camera()

    def setup(self):
        self.window.show_view(gameplay)
        # Set bg color to dark white
        arcade.set_background_color((0, 0, 0, 1))

        # Camera
        self.camera = arcade.Camera2D(projection=arcade.XYWH(0.0, 0.0, 800.0, 600.0))

        # Hide mouse
        self.window.set_mouse_visible(False)

        # Window Switch
        self.black = arcade.Sprite('assets/GLOBAL/black.png')
        self.black.position = WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2
        self.screen_switch = True
        self.switch_in = True
        self.screen_to_switch = None

        # Load custom cursor
        self.cursor = arcade.Sprite('assets/GLOBAL/cursor.png')
        self.cursor.scale = 4

        # Setup mouse tracking variables
        self.mouse_x = -32
        self.mouse_y = -32
        self.cursor_visible = True

    def on_draw(self):
        with self.camera.activate():
            self.window.clear()
            if self.cursor_visible:
                arcade.draw_sprite(self.cursor, pixelated=True)
            arcade.draw_sprite(self.black)

    def on_update(self, delta_time):
        x_, y_, _ = self.camera.unproject((self.mouse_x, self.mouse_y))
        if self.screen_switch:
            if self.switch_in:
                self.black.alpha = max(self.black.alpha - 8, 0)
            else:
                self.black.alpha = min(self.black.alpha + 8, 255)
            if self.black.alpha < 5 and self.switch_in:
                self.screen_switch = False
                self.switch_in = False
                self.black.alpha = 0
            if self.black.alpha > 250 and not self.switch_in:
                self.screen_switch = False
                self.black.alpha = 255
                if self.screen_to_switch == 'Folder Selection':
                    pass
                    # self.window.show_view(folder_selection)

        # Move cursor to mouse position
        self.cursor.position = x_ + 16, y_ - 16

    def on_mouse_press(self, x, y, button, modifiers):
        x_, y_, _ = self.camera.unproject((x, y))
        if not self.screen_switch:
            pass
            # if arcade.get_sprites_at_point((x_, y_), self.start_button):
            #     self.screen_switch = True
            #     self.screen_to_switch = 'Folder Selection'
            # if arcade.get_sprites_at_point((x_, y_), self.exit_button):
            #     arcade.exit()

    def on_resize(self, width, height):
        self.adjust_camera()

    def adjust_camera(self):
        height = self.window.height
        width = self.window.width
        if height / 3.0 < width / 4.0:
            h = height
            w = 4.0 / 3.0 * height
        else:
            h = 3.0 / 4.0 * width
            w = width

        self.camera.viewport = arcade.XYWH(width / 2.0, height / 2.0, w, h)
        self.camera.position = self.camera.width / 2.0, self.camera.height / 2.0

    def on_mouse_motion(self, x, y, dx, dy):
        self.mouse_x = x
        self.mouse_y = y

    def on_mouse_enter(self, x, y):
        self.cursor_visible = True
        self.window.set_mouse_visible(False)
        self.mouse_x = x
        self.mouse_y = y

    def on_mouse_leave(self, x, y):
        self.cursor_visible = False
        self.window.set_mouse_visible(True)


class Gameplay(arcade.View):
    def __init__(self):
        # Run Setup function with all setup in it
        super().__init__()

        # Early setup for variables.
        self.particles = None
        self.flame_texture_num = None
        self.obs = None
        self.obs = None
        self.bg = None
        self.dash = None
        self.flame_timer = None
        self.flame = None
        self.flame = None
        self.k = None
        self.camera_controller = None
        self.spirit = None
        self.cursor_visible = None
        self.cursor_visible = None
        self.mouse_y = None
        self.mouse_x = None
        self.cursor = None
        self.screen_switch = None
        self.screen_to_switch = None
        self.screen_to_switch = None
        self.switch_in = None
        self.black = None
        self.camera = None

    def on_show_view(self):
        self.setup()
        self.adjust_camera()

    def setup(self):
        # Set bg color to dark white
        arcade.set_background_color((0, 0, 0, 1))

        # Set Update rate
        self.window.set_update_rate(0.00001)
        self.window.set_draw_rate(0.00000001)

        # Camera
        self.camera = arcade.Camera2D(projection=arcade.XYWH(0.0, 0.0, 800.0, 600.0))

        # Hide mouse
        self.window.set_mouse_visible(False)

        # Window Switch
        self.black = arcade.Sprite('assets/GLOBAL/black.png')
        self.black.position = WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2
        self.screen_switch = True
        self.switch_in = True
        self.screen_to_switch = None

        # Load custom cursor
        self.cursor = arcade.Sprite('assets/GLOBAL/cursor.png')
        self.cursor.scale = 4

        # Setup mouse tracking variables
        self.mouse_x = -32
        self.mouse_y = -32
        self.cursor_visible = True

        # Load spirit
        self.spirit = arcade.Sprite('assets/gameplay/spirit.png')
        self.spirit.scale = 5
        self.spirit.position = 0, 0
        self.spirit.x_speed = 0.0
        self.spirit.y_speed = 0.0

        # Match camera to player
        self.camera.position = self.spirit.position
        self.black.position = self.camera.position

        # Setup Camera Controller
        self.camera_controller = CameraController(self.camera, self.spirit, 0.1)

        # Particles
        self.particles = arcade.SpriteList()

        # Flame
        self.flame = arcade.Sprite('assets/gameplay/s1.png')
        self.flame.append_texture(arcade.load_texture('assets/gameplay/s2.png'))
        self.flame.append_texture(arcade.load_texture('assets/gameplay/s3.png'))
        self.flame.append_texture(arcade.load_texture('assets/gameplay/s4.png'))
        self.flame.scale = 3
        self.flame.angle = 90
        self.flame.position = self.spirit.position[0], self.spirit.position[1] - 25
        self.flame_timer = 0
        self.flame_texture_num = 0

        # Setup key presses
        self.dash = False
        # Load level

        self.bg = arcade.Sprite('assets/bg{}.png'.format(level))
        self.bg.scale = 10
        self.bg.position = 0, self.bg.height - level_data[level]['offset']

        self.obs = arcade.SpriteList()
        for i in range(1, level_data[level]['obs'] + 1):
            temp = arcade.Sprite('assets/obs{}-{}.png'.format(level, i))
            temp.hitbox = arcade.hitbox.HitBox(arcade.hitbox.calculate_hit_box_points_detailed(
                Image.open('assets/obs{}-{}.png'.format(level, i))))
            temp.scale = 10
            temp.position = 0, temp.height - level_data[level]['offset']
            self.obs.append(temp)
        self.k = arcade.SpriteList()

        for i in range(1, level_data[level]['k'] + 1):
            temp = arcade.Sprite('assets/k{}-{}.png'.format(level, i))
            temp.hitbox = arcade.hitbox.HitBox(arcade.hitbox.calculate_hit_box_points_detailed(
                Image.open('assets/k{}-{}.png'.format(level, i))))
            temp.scale = 10
            temp.position = 0, temp.height - level_data[level]['offset']
            self.k.append(temp)

        # Allow to track FPS
        arcade.enable_timings()

        arcade.schedule(self.create_particle, 0.3)

    def on_draw(self):
        with self.camera.activate():
            self.window.clear()
            arcade.draw_sprite(self.bg, pixelated=True)
            self.obs.draw(pixelated=True)
            self.k.draw(pixelated=True)
            self.k.draw_hit_boxes((0, 0, 0, 225), 3)
            self.particles.draw(pixelated=True)
            if self.dash:
                arcade.draw_sprite(self.flame, pixelated=True)
            else:
                arcade.draw_sprite(self.spirit, pixelated=True)
            if self.cursor_visible:
                arcade.draw_sprite(self.cursor, pixelated=True)
            arcade.draw_sprite(self.black)
            arcade.Text('FPS: ' + str(round(arcade.get_fps())), self.camera.position[0] - 380,
                        self.camera.position[1] - 280, font_name='SF Pixelate Shaded Bold', font_size=20).draw()

    def on_update(self, delta_time):
        x_, y_, _ = self.camera.unproject((self.mouse_x, self.mouse_y))
        if self.screen_switch:
            if self.switch_in:
                self.black.alpha = max(self.black.alpha - 15, 0)
            else:
                self.black.alpha = min(self.black.alpha + 15, 255)
            if self.black.alpha < 5 and self.switch_in:
                self.screen_switch = False
                self.switch_in = False
                self.black.alpha = 0
            if self.black.alpha > 250 and not self.switch_in:
                self.screen_switch = False
                self.black.alpha = 255
                if self.screen_to_switch == 'hh':
                    pass

        if arcade.check_for_collision_with_list(self.spirit, self.obs):
            self.spirit.x_speed *= -1.5
        self.update_spirit()
        self.spirit.update()
        self.spirit.position = self.spirit.position[0], max(self.spirit.position[1], level_data[level]['lowest'])

        # Update flame
        self.flame_timer += delta_time
        if self.flame_timer > 0.1:
            self.flame_texture_num += 1
            self.flame_texture_num %= 4
            self.flame_timer = 0
        self.flame.position = self.spirit.position[0], self.spirit.position[1] - 25
        self.flame.set_texture(self.flame_texture_num)

        self.camera_controller.update()

        if self.particles:
            for particle in self.particles:
                particle.lifetime -= 1
                particle.scale = tuple(particle.scale)[0] - 5 / 200
                particle.alpha -= 230 / 50
                if particle.lifetime <= 0:
                    particle.kill()

        # Move cursor to mouse position
        self.cursor.position = x_ + 16, y_ - 16

        # Update cover
        self.black.position = self.camera.position

    def on_mouse_press(self, x, y, button, modifiers):
        x_, y_, _ = self.camera.unproject((x, y))
        if not self.screen_switch:
            pass
            # if arcade.get_sprites_at_point((x_, y_), self.start_button):
            #     self.screen_switch = True
            #     self.screen_to_switch = 'Folder Selection'
            # if arcade.get_sprites_at_point((x_, y_), self.exit_button):
            #     arcade.exit()

    def on_key_press(self, symbol, modifiers):
        if symbol == arcade.key.UP or symbol == arcade.key.W:
            self.dash = True

    def on_key_release(self, symbol, modifiers):
        if symbol == arcade.key.LEFT or symbol == arcade.key.A:
            self.spirit.x_speed = 5
            self.spirit.y_speed = 7
        if symbol == arcade.key.RIGHT or symbol == arcade.key.D:
            self.spirit.x_speed = -5
            self.spirit.y_speed = 7
        if symbol == arcade.key.UP or symbol == arcade.key.W:
            self.dash = False

    def on_resize(self, width, height):
        self.adjust_camera()

    def adjust_camera(self):
        height = self.window.height
        width = self.window.width
        if height / 3.0 < width / 4.0:
            h = height
            w = 4.0 / 3.0 * height
        else:
            h = 3.0 / 4.0 * width
            w = width

        self.camera.viewport = arcade.XYWH(width / 2.0, height / 2.0, w, h)

    def on_mouse_motion(self, x, y, dx, dy):
        self.mouse_x = x
        self.mouse_y = y

    def on_mouse_enter(self, x, y):
        self.cursor_visible = True
        self.window.set_mouse_visible(False)
        self.mouse_x = x
        self.mouse_y = y

    def on_mouse_leave(self, x, y):
        self.cursor_visible = False
        self.window.set_mouse_visible(True)

    def create_particle(self, delta_time):
        particle = arcade.Sprite('assets/gameplay/spirit.png')
        particle.angle = self.spirit.angle
        particle.position = self.spirit.position
        particle.lifetime = 50
        particle.scale = 5
        particle.alpha = 230
        self.particles.append(particle)

    def update_spirit(self):
        if self.dash:
            self.spirit.change_x = 0
            self.spirit.change_y = 5
            self.spirit.y_speed = 0
        else:
            # Move player
            self.spirit.change_x = self.spirit.x_speed * -1
            self.spirit.change_y = self.spirit.y_speed
            self.spirit.x_speed *= 0.95
            self.spirit.y_speed -= 0.25
            self.spirit.angle -= self.spirit.x_speed * 2


class CameraController:
    def __init__(self, camera, target, lerp_factor=0.1):
        self.camera = camera
        self.target = target
        self.lerp_factor = lerp_factor  # Controls the speed of following

    def update(self):
        # Current camera position
        current_x, current_y = self.camera.position

        # Target position
        target_x, target_y = self.target.position

        # Apply lerp for smooth following
        new_camera_x = current_x + (target_x - current_x) * self.lerp_factor
        new_camera_y = current_y + (target_y - current_y) * self.lerp_factor

        # Update camera position
        self.camera.position = (new_camera_x, new_camera_y)


if __name__ == '__main__':
    WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE = 800, 600, 'Wandering Spirit'
    ASPECT_RATIO = WINDOW_WIDTH / WINDOW_HEIGHT
    win = arcade.Window(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE, resizable=True)
    homepage = Homepage()
    level_selection = LevelSelection()
    gameplay = Gameplay()
    win.show_view(homepage)
    arcade.run()

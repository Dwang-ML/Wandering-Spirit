# Import needed modules
import arcade
import webbrowser

# Load fonts
arcade.load_font('fonts/SFPixelate-Bold.ttf')
arcade.load_font('fonts/SFPixelateShaded-Bold.ttf')

# Basic
level = 1
level_data = {
    1: {'offset': 1600, 'lowest': -40, 'obs': 2, 'k': 1, 'highest': 900, 'name': 'Beginner\'s Trail'},
    2: {'offset': 1600, 'lowest': -40, 'obs': 2, 'k': 3, 'highest': 900, 'name': 'Left and Right'},
    3: {'offset': 2800, 'lowest': -40, 'obs': 6, 'k': 3, 'highest': 1300, 'name': 'A Baby\'s Night'},
    4: {'offset': 2900, 'lowest': -40, 'obs': 2, 'k': 2, 'highest': 900, 'name': 'Dash'},
    5: {'offset': 2900, 'lowest': -40, 'obs': 12, 'k': 19, 'highest': 3000, 'name': 'The Last Level'}
}


class Homepage(arcade.View):
    def __init__(self):
        # Run Setup function with all setup in it
        super().__init__()

        # Early setup for variables.
        self.bg_m = None
        self.p = None
        self.click = None
        self.bg = None
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

        # Redirect button
        temp = arcade.Sprite('assets/homepage/button.png')
        temp.position = WINDOW_WIDTH // 2, 200
        temp.scale = 0.3
        self.redirect = arcade.SpriteList()
        self.redirect.append(temp)

        # Load bg
        self.bg = arcade.Sprite('assets/homepage/bg.png')
        self.bg.position = WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 170
        self.bg.scale = 1
        self.bg.angle = -10

        # Load sounds
        self.click = arcade.Sound('sfx/button.wav')
        self.bg_m = arcade.Sound('music/joy_of_code.wav')
        self.p = self.bg_m.play(loop=True, volume=0.5)

    def on_draw(self):
        with self.camera.activate():
            self.window.clear()
            arcade.draw_sprite(self.bg, pixelated=True)
            self.buttons.draw(pixelated=True)
            self.redirect.draw(pixelated=True)
            arcade.Text('Wandering Spirit', WINDOW_WIDTH // 2,
                        400, font_name='SF Pixelate Bold', font_size=50,
                        color=arcade.color.BLUE_SAPPHIRE, anchor_x='center').draw()
            arcade.Text('Wandering Spirit', WINDOW_WIDTH // 2,
                        400, font_name='SF Pixelate Shaded Bold', font_size=50,
                        color=arcade.color.BLUEBERRY, anchor_x='center').draw()
            arcade.Text('PLAY', WINDOW_WIDTH // 2,
                        290, font_name='SF Pixelate Bold', font_size=30,
                        color=arcade.color.WHITE_SMOKE, anchor_x='center').draw()
            arcade.Text('HOW TO PLAY + INFO', WINDOW_WIDTH // 2,
                        190, font_name='SF Pixelate Bold', font_size=20,
                        color=arcade.color.WHITE_SMOKE, anchor_x='center').draw()
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
                self.click.play()
                self.bg_m.stop(self.p)
                self.screen_switch = True
                self.screen_to_switch = 'level_selection'
            if arcade.get_sprites_at_point((x_, y_), self.redirect):
                self.click.play()
                webbrowser.open('https://github.com/Dwang-ML/Wandering-Spirit/blob/main/README.md')

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

    def on_show_view(self):
        self.setup()

    def setup(self):
        self.window.show_view(gameplay)


class Gameplay(arcade.View):
    def __init__(self):
        # Run Setup function with all setup in it
        super().__init__()

        # Early setup for variables.
        self.player = None
        self.bg_music = None
        self.click = None
        self.bounce = None
        self.dash_sfx = None
        self.jump = None
        self.lose = None
        self.lose = None
        self.win = None
        self.board = None
        self.menu_button = None
        self.retry_button = None
        self.menu = None
        self.retry = None
        self.lost = None
        self.won = None
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

        # Allow to track FPS
        arcade.enable_timings()

    def on_show_view(self):
        self.setup()
        self.adjust_camera()

    def setup(self):
        # Set bg color to dark white
        arcade.set_background_color((0, 0, 0, 1))

        # Set Update rate
        self.window.set_update_rate(0.0000001)
        self.window.set_draw_rate(0.0000001)

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
            temp = arcade.Sprite(arcade.load_texture('assets/obs{}-{}.png'.format(level, i),
                                                     hit_box_algorithm=arcade.hitbox.algo_simple))
            temp.scale = 10
            temp.position = 0, temp.height - level_data[level]['offset']
            self.obs.append(temp)

        self.k = arcade.SpriteList()
        for i in range(1, level_data[level]['k'] + 1):
            temp = arcade.Sprite(
                arcade.load_texture('assets/k{}-{}.png'.format(level, i), hit_box_algorithm=arcade.hitbox.algo_simple))
            temp.scale = 10
            temp.position = 0, temp.height - level_data[level]['offset']
            self.k.append(temp)

        # Setup win/lose
        self.won = False
        self.lost = False
        self.retry = arcade.Sprite('assets/gameplay/retry.png')
        self.retry.append_texture(arcade.load_texture('assets/gameplay/continue.png'))
        self.retry.scale = 5

        self.menu = arcade.Sprite('assets/gameplay/menu.png')
        self.menu.scale = 5

        self.retry_button = arcade.SpriteList()
        self.retry_button.append(self.retry)

        self.menu_button = arcade.SpriteList()
        self.menu_button.append(self.menu)

        self.board = arcade.Sprite('assets/gameplay/board.png')
        self.board.scale = 5

        # Load sounds
        self.jump = arcade.Sound('sfx/jump.wav')
        self.win = arcade.Sound('sfx/win.wav')
        self.lose = arcade.Sound('sfx/lose.wav')
        self.dash_sfx = arcade.Sound('sfx/dash.wav')
        self.click = arcade.Sound('sfx/button.wav')
        self.bounce = arcade.Sound('sfx/bounce.wav')
        self.bg_music = arcade.Sound('music/insolence.wav')
        self.player = self.bg_music.play(loop=True, volume=0.5)

        arcade.schedule(self.create_particle, 0.3)

    def on_draw(self):
        with self.camera.activate():
            self.window.clear()
            arcade.draw_sprite(self.bg, pixelated=True)
            self.obs.draw(pixelated=True)
            self.k.draw(pixelated=True)
            self.particles.draw(pixelated=True)
            if self.dash and not self.lost:
                arcade.draw_sprite(self.flame, pixelated=True)
            else:
                arcade.draw_sprite(self.spirit, pixelated=True)
            if self.won or self.lost:
                arcade.draw_sprite(self.board, pixelated=True)
                self.retry_button.draw(pixelated=True)
            self.menu_button.draw(pixelated=True)
            if self.lost:
                arcade.Text('FAILED', self.camera.position[0] - 10,
                            self.camera.position[1] + 80, font_name='SF Pixelate Bold', font_size=40,
                            color=arcade.color.RED_BROWN, anchor_x='center').draw()
                arcade.Text('FAILED', self.camera.position[0] - 10,
                            self.camera.position[1] + 80, font_name='SF Pixelate Shaded Bold', font_size=40,
                            color=arcade.color.RED, anchor_x='center').draw()
            if self.won:
                arcade.Text('SUCCESS', self.camera.position[0] - 10,
                            self.camera.position[1] + 80, font_name='SF Pixelate Bold', font_size=40,
                            color=arcade.color.ARCADE_GREEN, anchor_x='center').draw()
                arcade.Text('SUCCESS', self.camera.position[0] - 10,
                            self.camera.position[1] + 80, font_name='SF Pixelate Shaded Bold', font_size=40,
                            color=arcade.color.GREEN_YELLOW, anchor_x='center').draw()
            if not (self.won or self.lost):
                arcade.Text(level_data[level]['name'], self.camera.position[0],
                            self.camera.position[1] + 260, font_name='SF Pixelate Shaded Bold', font_size=20,
                            anchor_x='center',
                            color=(225, 225, 225, 255)).draw()
                arcade.Text(level_data[level]['name'], self.camera.position[0],
                            self.camera.position[1] + 260, font_name='SF Pixelate Bold', font_size=20,
                            anchor_x='center', color=(0, 0, 0, 255)).draw()

            if self.cursor_visible:
                arcade.draw_sprite(self.cursor, pixelated=True)
            arcade.draw_sprite(self.black)
            arcade.Text('FPS: ' + str(round(arcade.get_fps())), self.camera.position[0] - 380,
                        self.camera.position[1] - 280, font_name='SF Pixelate Shaded Bold', font_size=20).draw()

    def on_update(self, delta_time):
        global level
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
                if self.screen_to_switch == 'homepage':
                    self.bg_music.stop(self.player)
                    self.window.show_view(homepage)
                if self.screen_to_switch == 'gameplay':
                    self.bg_music.stop(self.player)
                    self.window.show_view(gameplay)
        if not (self.won or self.lost):
            if arcade.check_for_collision_with_list(self.spirit, self.obs):
                self.bounce.play()
                self.spirit.x_speed *= -1.5
            if arcade.check_for_collision_with_list(self.spirit, self.k):
                self.lose.play()
                self.lost = True
            if self.spirit.position[1] > level_data[level]['highest']:
                self.win.play()
                self.won = True
            self.update_spirit()
            self.spirit.update()
            self.spirit.position = self.spirit.position[0], max(self.spirit.position[1], level_data[level]['lowest'])

            self.camera_controller.update()

        if not self.screen_switch:
            if self.lost:
                if not (self.spirit.position[1] < self.camera.position[1] - 320):
                    self.spirit.change_y = -6
                    self.spirit.change_x = 0
                    self.spirit.update()
                self.retry.set_texture(0)
                self.retry.position = self.camera.position[0], self.camera.position[1] - 60
                self.board.position = self.camera.position[0], self.camera.position[1]
                self.menu.position = self.camera.position[0], self.camera.position[1]
            if self.won:
                if not (self.spirit.position[1] > self.camera.position[1] + 320):
                    self.spirit.update()
                self.retry.set_texture(1)
                self.retry.position = self.camera.position[0], self.camera.position[1] - 60
                self.board.position = self.camera.position[0], self.camera.position[1]
                self.menu.position = self.camera.position[0], self.camera.position[1]

            # Update flame
        self.flame_timer += delta_time
        if self.flame_timer > 0.1:
            self.flame_texture_num += 1
            self.flame_texture_num %= 4
            self.flame_timer = 0
        self.flame.position = self.spirit.position[0], self.spirit.position[1] - 25
        self.flame.set_texture(self.flame_texture_num)

        # Update particles
        if self.particles:
            for particle in self.particles:
                particle.lifetime -= 1
                particle.scale = tuple(particle.scale)[0] - 5 / 200
                particle.alpha -= 230 / 50
                if particle.lifetime <= 0:
                    particle.kill()

        # Set the positions of buttons
        if not (self.won or self.lost):
            self.menu.position = self.camera.position[0] - 350, self.camera.position[1] + 250

        # Move cursor to mouse position
        self.cursor.position = x_ + 16, y_ - 16

        # Update cover
        self.black.position = self.camera.position

    def on_mouse_press(self, x, y, button, modifiers):
        global level
        x_, y_, _ = self.camera.unproject((x, y))
        if not self.screen_switch:
            if arcade.get_sprites_at_point((x_, y_), self.menu_button):
                self.click.play()
                self.screen_switch = True
                self.screen_to_switch = 'homepage'
                arcade.unschedule(self.create_particle)
                if self.won:
                    level += 1
            if arcade.get_sprites_at_point((x_, y_), self.retry_button):
                if self.won:
                    self.click.play()
                    level += 1
                    self.screen_switch = True
                    self.screen_to_switch = 'gameplay'
                    arcade.unschedule(self.create_particle)
                if self.lost:
                    self.click.play()
                    self.screen_switch = True
                    self.screen_to_switch = 'gameplay'
                    arcade.unschedule(self.create_particle)

    def on_key_press(self, symbol, modifiers):
        if symbol == arcade.key.UP or symbol == arcade.key.W:
            self.dash = True
            self.dash_sfx.play()

    def on_key_release(self, symbol, modifiers):
        if symbol == arcade.key.LEFT or symbol == arcade.key.A:
            self.spirit.x_speed = 7
            self.spirit.y_speed = 6
            self.jump.play()
        if symbol == arcade.key.RIGHT or symbol == arcade.key.D:
            self.spirit.x_speed = -7
            self.spirit.y_speed = 6
            self.jump.play()
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
            self.spirit.change_y = 8
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

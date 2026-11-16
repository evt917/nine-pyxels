import pyxel, sys, math, time

SCREEN_WIDTH = 256
SCREEN_HEIGHT = 192
TILE_SIZE = 8
LOW_GRAVITY_RADIUS = 5 * TILE_SIZE
FLASHING_RADIUS = 5 * TILE_SIZE
MAX_FALL_SPEED = 6

PLAYER_WIDTH = 8
PLAYER_HEIGHT = 16
PLAYER_SPEED = 2
JUMP_STRENGTH = 4.5
GRAVITY = 1/5
LOW_GRAVITY = 1/50
JUMP_PAD_BOOST = -10
ROTATING_SURFACE_SIZE = 5

ENEMY_WIDTH = PLAYER_WIDTH
ENEMY_HEIGHT = PLAYER_HEIGHT
ENEMY_SPEED = 1
ENEMY_JUMP_STRENGTH = 3
ENEMY_RESPAWN_TIME = 180

LEVEL_MAPS = {
    1: [
    "                  ZZZZZZZZZZZZZZZZ                                                                                    ",
    "                  1111111111111111                                                                                    ",
    "                                           1        SS1                                                               ",
    "                                      R         S     S                                                               ",
    "        S                        11111111111SSSSSS    S                                                               ",
    "        S                                       SS    S                                                               ",
    "        S                                             S   111         SS                                              ",
    "        S                                                 S          S                                                ",
    "        S                                                 S                      1          1                         ",
    "        S                                                 S                     SSS      1                            ",
    "        S                                                 S           J                 SSS     1                     ",
    "        SEE                                     1111      SSJ          1  1                                           ",
    "    11  SSS                                               1111111111111111                                            ",
    "    SS  SSS                                                                                                           ",
    "                                                                                                                      ",
    "                                       S               111111111111111111                                             ",
    "                                       11111111                       1                                               ",
    "                                                                      1                                               ",
    "                                                                      1                                               ",
    "                           11111                                      1                                               ",
    "                                                                      1                         S                     ",
    "                                                                      1S111                                           ",
    "                                                                      1                                               ",
    "             111111                                                   1                  111111J                      ",
    "                                                                      1                                               ",
    "                                                                                                                      ",
    "    111                                                                                                               ",
    "                                                                                M                                     ",
    "SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
    "1111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111",
    "LLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLL"
    ],
    2: [
        "   ZZ          11                                                    ",
        "   EZ                     111                                        ",
        "  111                                                                ",
        "                                                                     ",
        "                                      XXKXX                          ",
        "                                        M                            ",
        "                                                                     ",
        "                                                                     ",
        "                                      MMMMM                          ",
        "                                                                     ",
        "            R                                                        ",
        "          11111                                1                     ",
        "       SSSSS                                                         ",
        "                                                   1                 ",
        "                   X  X  X  X                                        ",
        "               1  MX  X  X  X                  M                     ",
        "        JJ          X  X  X  X           S                           ",
        "                     X  X  X  X SSS                                  ",
        "                                111                                  ",
        "        111                                  X                       ",
        "X      X                           XX         11                     ",
        "11111111                             111111111111                    ",
        "SSSSSSSSSSSSSSSSSSSSSSSSSS          1SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS",
        "11111111111111111111111111          111111111111111111111111111111111",
        "LLLLLLLLLLLLLLLLLLLLLLLLLL111111111LLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLL"
    ]
    , 3: [
        "                                                    11               ",
        "                                                                     ",
        "                                                                     ",
        "                                                                     ",
        "                                                                     ",
        "                                                                     ",
        "                                                                     ",
        "                                                                     ",
        "                                                                     ",
        "                 X X               X X      J                        ",
        "                  M       M         M      11              11        ",
        "                                                                     ",
        "          X X                                                        ",
        "           M                                                         ",
        "      111                                                            ",
        "                                                                     ",
        "SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS     ",
        "L  L L L L L L  L L L L L L L   L L    LL  L L   L L   L L L         ",
        "                                                               S    S",
        "                                                              1S    S",
        "                                X  X  X  X                    1S    S",
        "                                                              1S    S",
        "                                    D                         1S    S",
        "                                   MMMM                       1S    S",
        "                                                              1S    S",
        "                          XXX                                 1S    S",
        "                                                              1S    S",
        "                                         XXXX                 1S    S",
        "                                                              1S    S",
        "                           J                                        S",
        "                           111                                      S",
        "                                      M          M             11111",
        "                                                                     ",
        "                                                                     ",
        "                                                            J1111111R"
    ]
    ,
    4: [
        "    1                                                           ",
        "                           R                                  11",
        "             111           1111111111111111111111111111111111  1",
        "S    S                                                         1",
        "g     S                                                        1",
        "       S                                                       1",
        " g     S                                                       1",
        "   S    S                                                      1",
        "    S    S                                                     1",
        "    S    S                                                     1",
        " SSS    S                                                      1",
        "S      SS                                                      1",
        " S      S                                                      1",
        "  S      SSSSSSSSSS                                            1",
        " S                 S                                           1",
        " S                 S                                           1",
        "S  11  11          S                                           1",
        "S      SSSSSSSSSSSS                                            1",
        " S      Sg                                                     1",
        "  S      S                                                     1",
        "   S      S                                                    1",
        "    S      Sg                                                  1",
        "     S      S                                                  1",
        "      S      S                                                 1",
        "       S      Sg                                               1",
        "        S      S                                               1",
        "       S      S                                                1",
        "      S      Sg                                                1",
        "     S      S                                                  1",
        "    S      Sg                                                  1",
        "   S      S                                                    1",
        "  S      S                                                     1",
        " S      S                                                      1",
        "S                                                              1",
        "S                                                              1",
        "S                                                              1",
        "S                                                              1",
        "S                                                              1",
        "1111Z111LLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLL",
        "1111E111111111111111111111111111111111111111111111111111111111111"
    ],

    5: [
        "SSSSSSSSSSSSSSSSSS1      S  S                                        ",
        "             S    1      SE S                                        ",
        "             S    1      SSSS                                        ",
        "             S    1                   SSSSS                          ",
        "             S    1                  S     S   R                     ",
        "             S    1                  S      S  11                    ",
        "             S    1                 S       S          r             ",
        "             Sg   111111111111111111S   f   S        11111           ",
        "             111111111111111111111111       S                        ",
        "                                    S       S                        ",
        "                                     S     S            S11          ",
        "                                      SSSSS             SSS          ",
        "                                    111111111                        ",
        "                                                                     ",
        "                                                                     ",
        "                                                                     ",
        "                                                                     ",
        "                                                                     ",
        "            1     1     1     1     1     1     1     1     1     1  ",
        "                                                                     ",
        "     r     r     r     r     r     r     r     r     r     r     r   ",
        "111111KKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKK",
        "                                                                     ",
        "gSgSgSgSgSgSgSgSgSgSgSgSgSgSgSgSgSgSgSgSgSgSgSgSgSgSgSgSgSgSgSgSgSgSg",
        "LLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLL"
    ]
    , 6: [
"                                                               SSSSS            ",
"                                                                                ",
"                                                               Z E              ",
"                                                               11111            ",
"                                                                                ",
"                                                                                ",
"                                                                                ",
"                                                                                ",
"                                                                                ",
"                                                                                ",
"             111111111111                                                       ",
"                                                                                ",
"                                                                                ",
"                                                           K                    ",
"          1111111111111111111111111111111111111111111111111111111111111111111111",
"         1                                                                      ",
"        1                                                                       ",
"       1                                                                        ",
"      1                                                                         ",
"     1                                                                          ",
"    1                     iiiiii                                                ",
"                                                                                ",
"1                                                                               ",
" 1                        JJJJJJ                                                ",
"  1MMMMMMMMMMMMMMMMMMMMMMM111111                                                ",
"                                                                                ",
"                                   g                                            ",
"                                   g                                            ",
"                                   g                                            ",
"                                   g                                            ",
"                                   g                                            ",
"                                 iiiiii                                         ",
"                                   g                                            ",
"                                   g                                            ",
"                                   g                                            ",
"                                   g                                            ",
"                                   g                                            ",
"                            1JJJ1JJgJJJ1JJJ1                                    ",
"                             1i111igii111J1                                     ",
"                              1i1iigiii1J1                                      ",
"                               1JJJJJJJJ1                                       ",
"                                                                                ",
"                                                                                ",
"                                                                                ",
"                                                                                ",
"                                             gg                                 ",
"                                                   JJJJJJJJJJiiiJ               ",
"                                         S        S                             ",
"                                         S1iiiiii1S                             ",
"                                         S1   R  1S                             ",
"                                         S11111111S                             ",
"                                                                                ",
"                                                                                ",
"                                                                                ",
"                                                                                ",
"                                                                                ",
"                                                                                ",
"                                                                                ",
"i                                                                               ",
"                                                                                ",
"                                               11111111111111JJJJJJJJJJJJJJ JJJJ",
"111111111111111111111111111111111111111111111111                             111",
"                                                                                ",
"                                                                    1           ",
"                                                           1       111          ",
"                                                          111     11r11    1    ",
"                                                 1       11r11  1  111          ",
"                                                111    1  111       1           ",
"                                               11r11       1                    ",
"                                      1         111                             ",
"                                     111         1                              ",
"                                    11r11                                       ",
"                                     111                                        ",
"                                      1                                         ",
"                                                                                ",
"                                                                                ",
"111111111111111111111111111111111111111111111111111111111111111111111111111111111"
    ],
    7: ["                                                                               ZE",
        "                        1      11            111            g                  ZZ",
        "R                SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS   rS   ",
        "11111111111111111                                                          Sr    ",
    ],
    8: [
        "                    JJ        i i  i i i i i  i i   i i i i i i i i i i  i i i i",
        "                                                                                ",
        "                                                                                ",
        "                    JJ                                                          ",
        "                                                                                ",
        "                                                                                ",
        "                    JJ                                                          ",
        "                                                                                ",
        "                          MMMMMMMMMMMMMMMMMMMMMMMMMMMMM                         ",
        "                    JJ                   1                                      ",
        "                                         1                                      ",
        "                          MMMMMMMMMMMMMMMMMMMMMMMMMMMMM                         ",
        "                    JJ                                                          ",
        "                                                                                ",
        "                                                                                ",
        "                                                                                ",
        "                    JJ111111111111111111111111111111                  1111111111",
        "11111111111111111111111111111111111111111111111111111111          1111  ZE     1",
        "11111111111111111111111111111111111111111111111111111111  R             Z      1",
        "                                                       1111111111111111111111111"
    ],
    9: [
        "                                                          E                     ",
        "                                                          Z                     ",
        "                                                                                ",
        "                                                                                ",
        "                                                                                ",
        "                                                                                ",
        "                                                                                ",
        "                                                          g                     ",
        "                                                                                ",
        "        R                                                                       ",
        "                                                                                ",
        "                                                                                ",
        "                                                                                ",
        "                                                                                ",
        "                                                                                ",
        "                                                                                ",
        "                                                                   g            ",
        "                                                                                ",
        "                                                                                ",
        "                                                                                ",
        "                                                                                ",
        "                                                                                ",
        "                                                                                ",
        "                                                                                ",
        "                                                                                ",
        "                                                                                ",
        "                                                                                ",
        "JJJJ                                                                           ",
        "11111111111111111111111111111111111111111111111111111111111111111111111111111111"
    ]
}

PLAYER_START_POSITIONS = {
    1: (32, 32),
    2: (32, 32),
    3: (32, 32),
    4: (128, 0),
    5: (0, 32),
    6: (0, 500),
    7: (0, 0),
    8: (32, 32),
    9: (32, 32)
}

LEVEL_TITLES = {
    1: "The Basics",
    2: "Timing",
    3: "Underworld",
    4: "The Dropper",
    5: "Big Mess",
    6: "Enemies",
    7: "Impossible Jump",
    8: "Extreme Danger",
    9: "Defying Gravity"
}


class RotationZone:
    def __init__(self, x, y, size, game_map):
        self.tile_x = x // TILE_SIZE
        self.tile_y = y // TILE_SIZE

        self.map_width = len(game_map[0])
        self.map_height = len(game_map)

        self.area_size = ROTATING_SURFACE_SIZE
        self.top_left_x = max(0, self.tile_x - self.area_size // 2)
        self.top_left_y = max(0, self.tile_y - self.area_size // 2)

        self.center_x = x + size / 2
        self.center_y = y + size / 2

        self.radius = 5.0 * TILE_SIZE
        self.speed = math.pi / 90
        self.current_angle = 0

        self.tiles = []
        for row in range(self.area_size):
            for col in range(self.area_size):
                map_y = self.top_left_y + row
                map_x = self.top_left_x + col

                if map_y < self.map_height and map_x < self.map_width:

                    char = game_map[map_y][map_x]

                    if char in ['1', 'g', 'S', 'r']:
                         self.tiles.append({
                            'char': char,
                            'orig_x': map_x * TILE_SIZE,
                            'orig_y': map_y * TILE_SIZE,
                            'width': TILE_SIZE,
                            'height': TILE_SIZE,
                            'x': map_x * TILE_SIZE,
                            'y': map_y * TILE_SIZE,
                         })

class FlashingZone:
    def __init__(self, x, y):
        self.center_x = x + TILE_SIZE / 2
        self.center_y = y + TILE_SIZE / 2
        self.radius = FLASHING_RADIUS

class PlatformerGame:
    def __init__(self):
        pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT, title="platformer.io", fps=60)
        pyxel.mouse(True)

        self.COLORS = {
            'player': 7,
            'ground': 1,
            'sky': 12,
            'lava': 8,
            'spikes': 13,
            'jump_pad': 10,
            'moving_jump_pad': 9,
            'moving_platform': 15,
            'level_exit': 11,
            'moving_spikes': 13,
            'moving_exit': 11,
            'low_gravity_block': 6,
            'rotating_block': 5,
            'flashing_block': 0,
            'enemy': 8,
            'key': 10,
            'door': 1,
        }

        self.setup_tint_sprite()
        self.game_state = "menu"
        self.selected_level = 1
        self.menu_cursor = 0

        # Timer / high score state
        self.run_start_time = None        # float: perf_counter when run started
        self.run_end_time = None          # float: perf_counter when run ended
        self.timer_running = False
        self.run_finished = False
        self.current_run_time_ms = 0      # integer milliseconds
        self.highscore_file = "highscore.txt"
        self.highscore_ms = self.load_highscore()  # None or int milliseconds
        
        # Track if speedrun timer should be active (only if started at level 1)
        self.speedrun_enabled = False
        self.death_count = 0              # Track deaths for the run

        pyxel.run(self.update, self.draw)

    

    def setup_tint_sprite(self):

        TINT_COLOR = 7
        TINT_PATTERN_SKIP_COLOR = 1

        for row in range(TILE_SIZE):
            for col in range(TILE_SIZE):
                if (row + col) % 2 == 0:
                    pyxel.pset(col, row, TINT_COLOR)
                else:
                    pyxel.pset(col, row, TINT_PATTERN_SKIP_COLOR)

        self.TINT_SPRITE_U = 0  
        self.TINT_SPRITE_V = 0
        self.TINT_COLOR = TINT_COLOR
        self.TINT_KEY_COLOR = TINT_PATTERN_SKIP_COLOR

    # ---------------- Timer / Highscore helpers ----------------
    def format_time_ms(self, ms):
        """Return MM:SS.mmm for milliseconds integer."""
        total_seconds = ms // 1000
        minutes = total_seconds // 60
        seconds = total_seconds % 60
        milliseconds = ms % 1000
        return f"{minutes:02d}:{seconds:02d}.{milliseconds:03d}"

    def load_highscore(self):
        """Load high score (best time in ms) from disk. Returns None if not found."""
        try:
            with open(self.highscore_file, "r") as f:
                val = int(f.read().strip())
                return val
        except Exception:
            return None

    def save_highscore(self, ms):
        """Save new high score (ms) to disk."""
        try:
            with open(self.highscore_file, "w") as f:
                f.write(str(int(ms)))
            self.highscore_ms = int(ms)
        except Exception:
            pass

    def start_run_timer(self):
        """Start the run timer if not already running and speedrun is enabled."""
        if self.speedrun_enabled and not self.timer_running and not self.run_finished:
            self.run_start_time = time.perf_counter()
            self.timer_running = True

    def end_run(self):
        """Call this when the player finishes the final level (after level 9)."""
        if self.run_finished:
            return
        if self.timer_running and self.run_start_time is not None:
            self.run_end_time = time.perf_counter()
            elapsed = (self.run_end_time - self.run_start_time) * 1000.0
            self.current_run_time_ms = int(elapsed)
            self.timer_running = False
            self.run_finished = True

            # Update high score if better (lower) or if none exists
            if self.highscore_ms is None or self.current_run_time_ms < self.highscore_ms:
                self.save_highscore(self.current_run_time_ms)

    # ----------------------------------------------------------

    def load_level(self, level_num):
        self.current_level = level_num

        level_rows = LEVEL_MAPS[level_num]
        self.level_map = [list(row) for row in level_rows]

        start_x, start_y = PLAYER_START_POSITIONS[level_num]
        self.player_x = start_x
        self.player_y = start_y
        self.player_vel_y = 0
        self.player_vel_x = 0
        self.on_ground = False
        self.start_pos = (start_x, start_y)
        self.is_rotating = False
        self.rotation_angle = 0
        self.has_key = False
        self.door_pos = None

        self.moving_platforms = []
        self.moving_spikes = []
        self.moving_jump_pads = []
        self.moving_exits = []
        self.lava_blobs = []
        self.low_gravity_blocks = []
        self.rotating_zones = []
        self.flashing_zones = []
        self.enemies = []
        self.enemy_states = []

        self.spawn_moving_objects()
        self.spawn_lava()
        self.spawn_special_blocks()
        self.spawn_enemies()

    def _create_enemy(self, x, y):
        return {
            'x': x,
            'y': y,
            'width': ENEMY_WIDTH,
            'height': ENEMY_HEIGHT,
            'vel_x': 0,
            'vel_y': 0,
            'on_ground': False,
            'facing': 1,
            'is_jumping': False,
        }

    def spawn_enemies(self):
        self.enemies = []
        self.enemy_states = []

        for y, row in enumerate(self.level_map):
            for x, tile in enumerate(row):
                if tile == 'i':
                    spawn_x = x * TILE_SIZE
                    spawn_y = y * TILE_SIZE

                    initial_enemy = self._create_enemy(spawn_x, spawn_y)

                    self.enemy_states.append({
                        'spawn_x': spawn_x,
                        'spawn_y': spawn_y,
                        'enemy': initial_enemy,
                        'respawn_timer': 0,
                    })

                    self.enemies.append(initial_enemy)

    def spawn_special_blocks(self,):

        for y, row in enumerate(self.level_map):
            for x, tile in enumerate(row):
                if tile == 'g':
                    self.low_gravity_blocks.append({
                        'x': x * TILE_SIZE,
                        'y': y * TILE_SIZE,
                        'width': TILE_SIZE,
                        'height': TILE_SIZE,
                    })
                elif tile == 'r':

                    self.rotating_zones.append(RotationZone(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, LEVEL_MAPS[self.current_level]))
                elif tile == 'f':
                    self.flashing_zones.append(FlashingZone(x * TILE_SIZE, y * TILE_SIZE))
                elif tile == 'Z':
                    self.door_pos = {'x': x * TILE_SIZE, 'y': y * TILE_SIZE, 'tile_x': x, 'tile_y': y}

    def spawn_lava(self):
        for y, row in enumerate(self.level_map):
            for x, tile in enumerate(row):
                if tile == 'L':

                    self.lava_blobs.append({
                        'x': x * TILE_SIZE,
                        'y': y * TILE_SIZE,
                        'width': TILE_SIZE,
                        'height': TILE_SIZE,
                        'move_timer': 0,
                        'dir': 1,
                    })

    def spawn_moving_objects(self):
        for y, row in enumerate(self.level_map):
            for x, tile in enumerate(row):
                if tile == 'M':
                    self.moving_platforms.append({
                        'x': x * TILE_SIZE,
                        'y': y * TILE_SIZE,
                        'width': TILE_SIZE * 4,
                        'height': TILE_SIZE,
                        'speed': 0.5,
                        'dir': 1,
                        'start_x': x * TILE_SIZE,
                        'end_x': x * TILE_SIZE + 4 * TILE_SIZE
                    })
                elif tile == 'X':
                    self.moving_spikes.append({
                        'x': x * TILE_SIZE,
                        'y': y * TILE_SIZE,
                        'width': TILE_SIZE,
                        'height': TILE_SIZE,
                        'speed': 0.5,
                        'dir': 1,
                        'start_x': x * TILE_SIZE,
                        'end_x': x * TILE_SIZE + 8 * TILE_SIZE
                    })
                elif tile == 'K':
                    self.moving_jump_pads.append({
                        'x': x * TILE_SIZE,
                        'y': y * TILE_SIZE,
                        'width': TILE_SIZE,
                        'height': TILE_SIZE,
                        'speed': 0.5,
                        'dir': 1,
                        'start_x': x * TILE_SIZE,
                        'end_x': x * TILE_SIZE + 10 * TILE_SIZE
                    })
                elif tile == 'D':
                    self.moving_exits.append({
                        'x': x * TILE_SIZE,
                        'y': y * TILE_SIZE,
                        'width': TILE_SIZE,
                        'height': TILE_SIZE,
                        'speed': 0.75,
                        'dir': 1,

                        'start_y': y * TILE_SIZE - 4 * TILE_SIZE,
                        'end_y': y * TILE_SIZE + 4 * TILE_SIZE
                    })

    def is_solid(self, x, y):
        tile_x = int(x // TILE_SIZE)
        tile_y = int(y // TILE_SIZE)

        if tile_x < 0 or tile_x >= len(self.level_map[0]) or tile_y < 0 or tile_y >= len(self.level_map):
            return False
        try:
            tile_char = self.level_map[tile_y][tile_x]
        except IndexError:
            return True

        if tile_char in ['1', 'M', 'K', 'D', 'E', 'S', 'L', 'J', 'g', 'r', 'f', 'R']:
            return True

        if tile_char == 'Z' and not self.has_key:
            return True

        return False

    def get_tile_char(self, x, y):
        tile_x = int(x // TILE_SIZE)
        tile_y = int(y // TILE_SIZE)
        if tile_x < 0 or tile_x >= len(self.level_map[0]) or tile_y < 0 or tile_y >= len(self.level_map):
            return None

        return self.level_map[tile_y][tile_x]

    def set_tile_char(self, x, y, char):
        tile_x = int(x // TILE_SIZE)
        tile_y = int(y // TILE_SIZE)
        if tile_x < 0 or tile_x >= len(self.level_map[0]) or tile_y < 0 or tile_y >= len(self.level_map):
            return

        self.level_map[tile_y][tile_x] = char

    def reset_player(self):
        self.player_x = self.start_pos[0]
        self.player_y = self.start_pos[1]
        self.player_vel_y = 0
        self.player_vel_x = 0
        self.is_rotating = False
        self.rotation_angle = 0
        self.death_count += 1

        if self.current_level in LEVEL_MAPS:
            self.load_level(self.current_level)

    def update_lava(self):
        new_lava_blobs = []

        for blob in self.lava_blobs:

            blob['move_timer'] += 1

            if blob['move_timer'] >= 60:
                blob['move_timer'] = 0

                check_x = blob['x'] + blob['width'] / 2
                check_y = blob['y'] + blob['height'] + 1

                is_supported_by_solid = self.get_tile_char(check_x, check_y) in ['1', 'S', 'g', 'r', 'f', 'i', 'R', 'Z']

                is_supported_by_lava = False
                for other_blob in self.lava_blobs:
                    if other_blob is blob: continue
                    if (blob['x'] < other_blob['x'] + other_blob['width'] and
                        blob['x'] + blob['width'] > other_blob['x'] and
                        blob['y'] + blob['height'] == other_blob['y']):
                        is_supported_by_lava = True
                        break

                if not is_supported_by_solid and not is_supported_by_lava:

                    blob['y'] += TILE_SIZE
                    new_lava_blobs.append(blob)
                else:

                    if blob['width'] >= TILE_SIZE * 2:

                        half_width = blob['width'] // 2

                        new_lava_blobs.append({
                            'x': blob['x'],
                            'y': blob['y'],
                            'width': half_width,
                            'height': blob['height'],
                            'move_timer': 0,
                            'dir': -1,
                        })

                        new_lava_blobs.append({
                            'x': blob['x'] + half_width,
                            'y': blob['y'],
                            'width': half_width,
                            'height': blob['height'],
                            'move_timer': 0,
                            'dir': 1,
                        })

                    else:

                        lava_stops = ['1', 'S', 'L', 'g', 'r', 'f', 'i', 'R', 'Z']
                        can_move_left = self.get_tile_char(blob['x'] - 1, blob['y']) not in lava_stops
                        can_move_right = self.get_tile_char(blob['x'] + blob['width'] + 1, blob['y']) not in lava_stops

                        next_x = blob['x'] + blob['dir'] * TILE_SIZE

                        if not can_move_left and blob['dir'] == -1:
                            blob['dir'] = 1
                            next_x = blob['x'] + blob['dir'] * TILE_SIZE
                        elif not can_move_right and blob['dir'] == 1:
                            blob['dir'] = -1
                            next_x = blob['x'] + blob['dir'] * TILE_SIZE

                        blob['x'] = next_x
                        new_lava_blobs.append(blob)

            else:

                new_lava_blobs.append(blob)

        self.lava_blobs = new_lava_blobs

    def _kill_enemy(self, state):
        state['enemy'] = None
        state['respawn_timer'] = ENEMY_RESPAWN_TIME

    def update_enemies(self):
        def is_obstacle(x, y):
            tile_char = self.get_tile_char(x, y)

            if tile_char in ['1', 'g', 'f', 'R']: return 'solid'

            if tile_char == 'Z': return 'solid'

            if tile_char == 'S': return 'hazard'
            if tile_char == 'r': return 'solid'
            if tile_char == 'L': return 'hazard'
            if tile_char == 'J': return 'jump_pad'

            for p in self.moving_platforms + self.moving_jump_pads + self.moving_exits:
                if (x < p['x'] + p['width'] and x > p['x'] and
                    y < p['y'] + p['height'] and y > p['y']):

                    return 'solid' if p in self.moving_platforms + self.moving_exits else 'jump_pad'

            for s in self.moving_spikes:
                if (x < s['x'] + s['width'] and x > s['x'] and
                    y < s['y'] + s['height'] and y > s['y']):
                    return 'hazard'

            for zone in self.rotating_zones:
                for tile in zone.tiles:
                    if (x < tile['x'] + tile['width'] and x > tile['x'] and
                        y < tile['y'] + tile['height'] and y > tile['y']):
                        return 'solid' if tile['char'] in ['1', 'g', 'f', 'r'] else 'hazard' if tile['char'] == 'S' else 'none'

            return 'none'

        for enemy in self.enemies:
            if (self.player_x < enemy['x'] + enemy['width'] and
                self.player_x + PLAYER_WIDTH > enemy['x'] and
                self.player_y < enemy['y'] + enemy['height'] and
                self.player_y + PLAYER_HEIGHT > enemy['y']):
                self.reset_player()
                return

        updated_enemies = []

        for state in self.enemy_states:

            if state['enemy'] is None:

                if state['respawn_timer'] > 0:
                    state['respawn_timer'] -= 1

                if state['respawn_timer'] == 0:
                    new_enemy = self._create_enemy(state['spawn_x'], state['spawn_y'])
                    state['enemy'] = new_enemy

            if state['enemy'] is not None:
                enemy = state['enemy']

                enemy_center_x = enemy['x'] + enemy['width'] / 2
                enemy_center_y = enemy['y'] + enemy['height'] / 2
                current_gravity = GRAVITY
                for block in self.low_gravity_blocks:
                    if (enemy_center_x > block['x'] - LOW_GRAVITY_RADIUS and
                        enemy_center_x < block['x'] + block['width'] + LOW_GRAVITY_RADIUS and
                        enemy_center_y > block['y'] - LOW_GRAVITY_RADIUS and
                        enemy_center_y < block['y'] + block['height'] + LOW_GRAVITY_RADIUS):
                        current_gravity = LOW_GRAVITY
                        break

                if enemy['y'] > len(self.level_map) * TILE_SIZE:

                    self._kill_enemy(state)
                    continue

                target_x = self.player_x

                is_lethal_hazard_ahead = False

                check_x = enemy['x'] + enemy['facing'] * enemy['width'] + enemy['facing'] * 1

                check_y_ground = enemy['y'] + enemy['height'] + 1

                tile_char = self.get_tile_char(check_x, check_y_ground)
                if tile_char in ['S', 'L']:
                    is_lethal_hazard_ahead = True

                if not is_lethal_hazard_ahead:

                    for s in self.moving_spikes:
                        if (check_x < s['x'] + s['width'] and
                            check_x > s['x'] and
                            check_y_ground < s['y'] + s['height'] and
                            check_y_ground > s['y']):
                            is_lethal_hazard_ahead = True
                            break

                if not is_lethal_hazard_ahead:
                     for blob in self.lava_blobs:
                        if (check_x < blob['x'] + blob['width'] and
                            check_x > blob['x'] and
                            check_y_ground < blob['y'] + blob['height'] and
                            check_y_ground > blob['y']):
                            is_lethal_hazard_ahead = True
                            break

                if not is_lethal_hazard_ahead:
                    for zone in self.rotating_zones:
                        for tile in zone.tiles:
                            if tile['char'] == 'S':

                                if (check_x < tile['x'] + tile['width'] and check_x > tile['x'] and
                                    check_y_ground < tile['y'] + tile['height'] and check_y_ground > tile['y']):
                                    is_lethal_hazard_ahead = True
                                    break
                        if is_lethal_hazard_ahead: break

                if is_lethal_hazard_ahead:

                    enemy['vel_x'] = 0
                    enemy['facing'] *= -1

                elif abs(target_x - enemy['x']) > ENEMY_WIDTH / 2:
                    if target_x > enemy['x']:
                        enemy['facing'] = 1

                        enemy['vel_x'] = min(enemy['vel_x'] + 0.2, ENEMY_SPEED)
                    else:
                        enemy['facing'] = -1

                        enemy['vel_x'] = max(enemy['vel_x'] - 0.2, -ENEMY_SPEED)
                else:

                    enemy['vel_x'] *= 0.85
                    if abs(enemy['vel_x']) < 0.1:
                         enemy['vel_x'] = 0

                next_step_x_check = enemy['x'] + (enemy['width'] if enemy['facing'] == 1 else 0) + enemy['facing'] * 2
                check_y_mid = enemy['y'] + enemy['height'] / 2
                obstacle = is_obstacle(next_step_x_check, check_y_mid)

                should_jump = False

                if obstacle in ['solid', 'jump_pad']:
                    should_jump = True

                if should_jump and enemy['on_ground'] and not enemy['is_jumping']:
                    enemy['vel_y'] = -ENEMY_JUMP_STRENGTH
                    enemy['on_ground'] = False
                    enemy['is_jumping'] = True

                enemy['x'] += enemy['vel_x']
                enemy['vel_y'] += current_gravity
                enemy['y'] += enemy['vel_y']

                enemy['on_ground'] = False

                hazard_hit = False

                for s in self.moving_spikes:
                    if (enemy['x'] < s['x'] + s['width'] and
                        enemy['x'] + enemy['width'] > s['x'] and
                        enemy['y'] < s['y'] + s['height'] and
                        enemy['y'] + enemy['height'] > s['y']):
                        self._kill_enemy(state)
                        hazard_hit = True
                        break
                if hazard_hit: continue

                for blob in self.lava_blobs:
                     if (enemy['x'] < blob['x'] + blob['width'] and
                         enemy['x'] + enemy['width'] > blob['x'] and
                         enemy['y'] < blob['y'] + blob['height'] and
                         enemy['y'] + enemy['height'] > blob['y']):
                         self._kill_enemy(state)
                         hazard_hit = True
                         break
                if hazard_hit: continue

                collided_points = []
                landed_on_jump_pad = False

                for x_check in [enemy['x'], enemy['x'] + enemy['width'] - 1]:

                    y_check = enemy['y'] + enemy['height'] + 1
                    tile_char = self.get_tile_char(x_check, y_check)

                    if tile_char in ['1', 'g', 'f', 'r', 'R', 'Z']:
                         collided_points.append(y_check)
                    elif tile_char == 'S' and enemy['vel_y'] >= 0:
                         self._kill_enemy(state)
                         hazard_hit = True
                         break
                    elif tile_char == 'J' and enemy['vel_y'] >= 0:
                         landed_on_jump_pad = True
                         collided_points.append(y_check)

                if hazard_hit: continue

                for p in self.moving_platforms + self.moving_jump_pads:

                    if (enemy['x'] < p['x'] + p['width'] and
                        enemy['x'] + enemy['width'] > p['x'] and
                        enemy['y'] + enemy['height'] >= p['y'] and
                        enemy['y'] + enemy['height'] < p['y'] + p['height'] and
                        enemy['vel_y'] >= 0):

                        old_enemy_bottom = enemy['y'] - enemy['vel_y'] + enemy['height']
                        if old_enemy_bottom <= p['y']:
                            collided_points.append(p['y'] + 1)
                            if p in self.moving_jump_pads:
                                landed_on_jump_pad = True

                for zone in self.rotating_zones:
                    for tile in zone.tiles:
                        if (enemy['x'] < tile['x'] + tile['width'] and
                            enemy['x'] + enemy['width'] > tile['x'] and
                            enemy['y'] + enemy['height'] >= tile['y'] and
                            enemy['y'] + enemy['height'] < tile['y'] + tile['height'] and
                            enemy['vel_y'] >= 0):

                            old_enemy_bottom = enemy['y'] - enemy['vel_y'] + enemy['height']

                            if old_enemy_bottom <= tile['y']:
                                if tile['char'] == 'S':
                                    self._kill_enemy(state)
                                    hazard_hit = True
                                    break

                                collided_points.append(tile['y'] + 1)
                    if hazard_hit: break
                if hazard_hit: continue

                if collided_points and enemy['vel_y'] >= 0:
                    landing_y = min(collided_points) - 1

                    enemy['y'] = (landing_y // TILE_SIZE) * TILE_SIZE - enemy['height']
                    enemy['vel_y'] = 0
                    enemy['on_ground'] = True
                    enemy['is_jumping'] = False

                    if landed_on_jump_pad:
                        enemy['vel_y'] = JUMP_PAD_BOOST
                        enemy['on_ground'] = False

                if enemy['vel_y'] < 0:
                    for x, y in [(enemy['x'], enemy['y']),
                                 (enemy['x'] + enemy['width'] - 1, enemy['y'])]:

                        if self.get_tile_char(x, y) in ['1', 'g', 'f', 'R', 'Z']:
                            enemy['y'] = (int(y // TILE_SIZE) + 1) * TILE_SIZE
                            enemy['vel_y'] = 0
                            break

                        for zone in self.rotating_zones:
                            for tile in zone.tiles:
                                if tile['char'] in ['1', 'g', 'r', 'f'] and (
                                    x < tile['x'] + tile['width'] and
                                    x > tile['x'] and
                                    y < tile['y'] + tile['height'] and
                                    y > tile['y']):
                                    enemy['y'] = (int(y // TILE_SIZE) + 1) * TILE_SIZE
                                    enemy['vel_y'] = 0
                                    break
                            else:
                                continue
                            break

                updated_enemies.append(enemy)

        self.enemies = updated_enemies

    def update_menu(self):
        if pyxel.btnp(pyxel.KEY_UP):
            self.menu_cursor = max(0, self.menu_cursor - 1)
        if pyxel.btnp(pyxel.KEY_DOWN):
            self.menu_cursor = min(len(LEVEL_MAPS) - 1, self.menu_cursor + 1)
        if pyxel.btnp(pyxel.KEY_RETURN) or pyxel.btnp(pyxel.KEY_SPACE):
            self.selected_level = self.menu_cursor + 1
            self.game_state = "playing"
            self.load_level(self.selected_level)
            # Start the run timer only if starting at level 1
            if self.selected_level == 1:
                self.speedrun_enabled = True
                self.death_count = 0
                self.start_run_timer()
            else:
                self.speedrun_enabled = False

    def draw_menu(self):
        pyxel.cls(1)  # Dark blue background
        pyxel.text(SCREEN_WIDTH//2 - 50, 10, "Platformer", 7)
        pyxel.text(SCREEN_WIDTH//2 - 50, 20, "Select the Level with Arrow Keys", 6)
        pyxel.text(SCREEN_WIDTH//2 - 50, 30, "Press Enter to Start", 6)
        pyxel.text(SCREEN_WIDTH//2 - 50, 40, "Press R anytime to reset to Level 1", 8)

        for i, level_num in enumerate(LEVEL_MAPS.keys()):
            y = 55 + i * 15
            level_title = LEVEL_TITLES.get(level_num, f"Level {level_num}")
            color = 10 if i == self.menu_cursor else 7
            pyxel.text(SCREEN_WIDTH//2 - 40, y, f"{level_num}. {level_title}", color)

            # Draw cursor
            if i == self.menu_cursor:
                pyxel.text(SCREEN_WIDTH//2 - 50, y, ">", 10)

    def update(self):
        # Start timer if playing
        if self.game_state == "playing":
            self.start_run_timer()
            # Check for R key to reset to level 1 with speedrun
            if pyxel.btnp(pyxel.KEY_R):
                self.game_state = "playing"
                self.selected_level = 1
                self.speedrun_enabled = True
                self.death_count = 0
                self.run_start_time = None
                self.run_end_time = None
                self.timer_running = False
                self.run_finished = False
                self.current_run_time_ms = 0
                self.load_level(1)
                self.start_run_timer()
                return

        if self.game_state == "menu":
            self.update_menu()
            return
        elif self.game_state == "complete":
            # allow restart to menu and reset run state
            if pyxel.btnp(pyxel.KEY_R):
                self.game_state = "menu"
                self.menu_cursor = 0
                # reset run timer state for a fresh run
                self.run_start_time = None
                self.run_end_time = None
                self.timer_running = False
                self.run_finished = False
                self.current_run_time_ms = 0
            return

        # Update the in-run timer each frame if running
        if self.timer_running and self.run_start_time is not None:
            elapsed = (time.perf_counter() - self.run_start_time) * 1000.0
            self.current_run_time_ms = int(elapsed)

        self.is_rotating = False
        current_zone = None
        player_center_x = self.player_x + PLAYER_WIDTH / 2
        player_center_y = self.player_y + PLAYER_HEIGHT / 2

        for zone in self.rotating_zones:
            zone.current_angle += zone.speed

            for tile in zone.tiles:

                orig_center_x = tile['orig_x'] + TILE_SIZE / 2
                orig_center_y = tile['orig_y'] + TILE_SIZE / 2

                rel_x = orig_center_x - zone.center_x
                rel_y = orig_center_y - zone.center_y

                new_rel_x = rel_x * math.cos(zone.current_angle) - rel_y * math.sin(zone.current_angle)
                new_rel_y = rel_x * math.sin(zone.current_angle) + rel_y * math.cos(zone.current_angle)

                new_center_x = zone.center_x + new_rel_x
                new_center_y = zone.center_y + new_rel_y

                tile['x'] = new_center_x - TILE_SIZE / 2
                tile['y'] = new_center_y - TILE_SIZE / 2

            dist_sq = (player_center_x - zone.center_x)**2 + (player_center_y - zone.center_y)**2
            if dist_sq < zone.radius**2:
                self.is_rotating = True
                current_zone = zone

        current_gravity = GRAVITY
        for block in self.low_gravity_blocks:

            if (player_center_x > block['x'] - LOW_GRAVITY_RADIUS and
                player_center_x < block['x'] + block['width'] + LOW_GRAVITY_RADIUS and
                player_center_y > block['y'] - LOW_GRAVITY_RADIUS and
                player_center_y < block['y'] + block['height'] + LOW_GRAVITY_RADIUS):
                current_gravity = LOW_GRAVITY
                break

        if not pyxel.btn(pyxel.KEY_LEFT) and not pyxel.btn(pyxel.KEY_RIGHT):
            self.player_vel_x *= 0.85
            if abs(self.player_vel_x) < 0.1:
                self.player_vel_x = 0

        if pyxel.btn(pyxel.KEY_LEFT):
            self.player_vel_x = max(self.player_vel_x - 0.5, -PLAYER_SPEED)
        if pyxel.btn(pyxel.KEY_RIGHT):
            self.player_vel_x = min(self.player_vel_x + 0.5, PLAYER_SPEED)

        self.player_x += self.player_vel_x

        # Wall jumping
        can_wall_jump_left = False
        can_wall_jump_right = False

        # Check for wall on left side
        for y_check in range(int(self.player_y), int(self.player_y + PLAYER_HEIGHT), TILE_SIZE//2):
            if self.is_solid(self.player_x - 1, y_check):
                can_wall_jump_left = True
                break

        # Check for wall on right side
        for y_check in range(int(self.player_y), int(self.player_y + PLAYER_HEIGHT), TILE_SIZE//2):
            if self.is_solid(self.player_x + PLAYER_WIDTH + 1, y_check):
                can_wall_jump_right = True
                break

        if pyxel.btnp(pyxel.KEY_UP) or pyxel.btnp(pyxel.KEY_SPACE):
            if self.on_ground:
                self.player_vel_y = -JUMP_STRENGTH
                self.on_ground = False
            elif can_wall_jump_left:
                self.player_vel_y = -JUMP_STRENGTH
                self.player_vel_x = PLAYER_SPEED * 0.8  # Boost right
                self.on_ground = False
            elif can_wall_jump_right:
                self.player_vel_y = -JUMP_STRENGTH
                self.player_vel_x = -PLAYER_SPEED * 0.8  # Boost left
                self.on_ground = False

        self.player_vel_y += current_gravity
        self.player_y += self.player_vel_y

        self.update_lava()

        for p in self.moving_platforms:
            p['x'] += p['speed'] * p['dir']
            if p['x'] > p['end_x'] or p['x'] < p['start_x']:
                p['dir'] *= -1

        for s in self.moving_spikes:
            s['x'] += s['speed'] * s['dir']
            if s['x'] > s['end_x'] or s['x'] < s['start_x']:
                s['dir'] *= -1

        for k in self.moving_jump_pads:
            k['x'] += k['speed'] * k['dir']
            if k['x'] > k['end_x'] or k['x'] < k['start_x']:
                k['dir'] *= -1

        for d in self.moving_exits:
            d['y'] += d['speed'] * d['dir']
            if d['y'] > d['end_y'] or d['y'] < d['start_y']:
                d['dir'] *= -1

        self.on_ground = False

        rotated_tile_coords = set()
        for zone in self.rotating_zones:
            for tile in zone.tiles:
                rotated_tile_coords.add((tile['orig_x'] // TILE_SIZE, tile['orig_y'] // TILE_SIZE))

        if current_zone:
            for tile in current_zone.tiles:

                if (self.player_x < tile['x'] + tile['width'] and
                    self.player_x + PLAYER_WIDTH > tile['x'] and
                    self.player_y + PLAYER_HEIGHT >= tile['y'] and
                    self.player_y + PLAYER_HEIGHT < tile['y'] + tile['height'] and
                    self.player_vel_y >= 0):

                    old_player_bottom = self.player_y - self.player_vel_y + PLAYER_HEIGHT

                    if old_player_bottom <= tile['y']:

                        if tile['char'] == 'S':
                            self.reset_player()
                            return

                        slip_force = math.sin(current_zone.current_angle) * 0.4
                        self.player_vel_x += slip_force

                        self.player_y = tile['y'] - PLAYER_HEIGHT
                        self.player_vel_y = 0
                        self.on_ground = True
                        break

        collided_points = []

        for x, y in [(self.player_x, self.player_y + PLAYER_HEIGHT),
                     (self.player_x + PLAYER_WIDTH - 1, self.player_y + PLAYER_HEIGHT),
                     (self.player_x, self.player_y),
                     (self.player_x, self.player_y + PLAYER_HEIGHT - 1),
                     (self.player_x + PLAYER_WIDTH - 1, self.player_y),
                     (self.player_x + PLAYER_WIDTH - 1, self.player_y + PLAYER_HEIGHT - 1)]:
            tile_char = self.get_tile_char(x, y)
            tile_x = int(x // TILE_SIZE)
            tile_y = int(y // TILE_SIZE)

            if (tile_x, tile_y) in rotated_tile_coords:
                continue

            if tile_char in ['1', 'g', 'f', 'R']:
                collided_points.append(y)

            elif tile_char == 'Z' and not self.has_key:
                collided_points.append(y)

            if tile_char == 'S':
                self.reset_player()
                return
            elif tile_char == 'J' and self.player_vel_y >= 0:
                self.player_vel_y = JUMP_PAD_BOOST
            elif tile_char == 'E':
                if self.has_key:
                    self.current_level += 1
                    if self.current_level in LEVEL_MAPS:
                        self.load_level(self.current_level)
                    else:
                        # Completed all levels: mark complete and end run
                        self.game_state = "complete"
                        self.end_run()

        if collided_points and self.player_vel_y >= 0:

            landing_tile_y_row = max(collided_points) // TILE_SIZE

            self.player_y = landing_tile_y_row * TILE_SIZE - PLAYER_HEIGHT
            self.player_vel_y = 0
            self.on_ground = True

        if self.player_vel_y < 0:

            for x, y in [(self.player_x, self.player_y),
                         (self.player_x + PLAYER_WIDTH - 1, self.player_y)]:
                tile_char = self.get_tile_char(x, y)
                tile_x = int(x // TILE_SIZE)
                tile_y = int(y // TILE_SIZE)

                if (tile_x, tile_y) in rotated_tile_coords:
                    continue

                if tile_char in ['1', 'g', 'f', 'R', 'Z']:

                    self.player_y = (int(y // TILE_SIZE) + 1) * TILE_SIZE
                    self.player_vel_y = 0
                    break

        for blob in self.lava_blobs:
             if (self.player_x < blob['x'] + blob['width'] and
                 self.player_x + PLAYER_WIDTH > blob['x'] and
                 self.player_y < blob['y'] + blob['height'] and
                 self.player_y + PLAYER_HEIGHT > blob['y']):
                 self.reset_player()
                 return

        for p in self.moving_platforms:
            if (self.player_x < p['x'] + p['width'] and
                self.player_x + PLAYER_WIDTH > p['x'] and
                self.player_y + PLAYER_HEIGHT >= p['y'] and
                self.player_y + PLAYER_HEIGHT < p['y'] + p['height'] and
                self.player_vel_y >= 0):

                old_player_bottom = self.player_y - self.player_vel_y + PLAYER_HEIGHT
                if old_player_bottom <= p['y']:

                    self.player_y = p['y'] - PLAYER_HEIGHT
                    self.player_vel_y = 0
                    self.on_ground = True
                    self.player_x += p['speed'] * p['dir']

        for s in self.moving_spikes:
            if (self.player_x < s['x'] + s['width'] and
                self.player_x + PLAYER_WIDTH > s['x'] and
                self.player_y < s['y'] + s['height'] and
                self.player_y + PLAYER_HEIGHT > s['y']):
                self.reset_player()
                return

        for k in self.moving_jump_pads:
            if (self.player_x < k['x'] + k['width'] and
                self.player_x + PLAYER_WIDTH > k['x'] and
                self.player_y + PLAYER_HEIGHT >= k['y'] and
                self.player_y + PLAYER_HEIGHT < k['y'] + k['height'] and
                self.player_vel_y >= 0):

                old_player_bottom = self.player_y - self.player_vel_y + PLAYER_HEIGHT
                if old_player_bottom <= k['y']:

                    self.player_y = k['y'] - PLAYER_HEIGHT
                    self.player_vel_y = JUMP_PAD_BOOST
                    self.on_ground = False
                    self.player_x += k['speed'] * k['dir']

        for d in self.moving_exits:
            if (self.player_x < d['x'] + d['width'] and
                self.player_x + PLAYER_WIDTH > d['x'] and
                self.player_y < d['y'] + d['height'] and
                self.player_y + PLAYER_HEIGHT > d['y']):

                self.current_level += 1
                if self.current_level in LEVEL_MAPS:
                    self.load_level(self.current_level)
                else:
                    # Some maps set current_level to "Complete" — treat as completion
                    self.current_level = "Complete"
                    self.game_state = "complete"
                    self.end_run()

        player_tile_x = int((self.player_x + PLAYER_WIDTH/2) // TILE_SIZE)
        player_tile_y = int((self.player_y + PLAYER_HEIGHT/2) // TILE_SIZE)

        if self.get_tile_char(player_tile_x * TILE_SIZE, player_tile_y * TILE_SIZE) == 'R':
             self.has_key = True
             self.set_tile_char(player_tile_x * TILE_SIZE, player_tile_y * TILE_SIZE, ' ')

        if self.door_pos and not self.has_key:
             pass
        elif self.door_pos and self.has_key:

             if (self.player_x < self.door_pos['x'] + TILE_SIZE and
                 self.player_x + PLAYER_WIDTH > self.door_pos['x'] and
                 self.player_y < self.door_pos['y'] + TILE_SIZE and
                 self.player_y + PLAYER_HEIGHT > self.door_pos['y']):

                 self.set_tile_char(self.door_pos['x'], self.door_pos['y'], ' ')

                 exit_x = self.door_pos['x'] + TILE_SIZE
                 exit_y = self.door_pos['y']

                 if (self.player_x < exit_x + TILE_SIZE and
                     self.player_x + PLAYER_WIDTH > exit_x and
                     self.player_y < exit_y + TILE_SIZE and
                     self.player_y + PLAYER_HEIGHT > exit_y):

                     self.current_level += 1
                     if self.current_level in LEVEL_MAPS:
                         self.load_level(self.current_level)
                     else:
                         self.current_level = "Complete"
                         self.game_state = "complete"
                         self.end_run()

        self.update_enemies()

        if self.player_y > len(self.level_map) * TILE_SIZE:
            self.reset_player()

    def draw_lava(self):
        """Draws the dynamic lava blobs."""
        for blob in self.lava_blobs:
            pyxel.rect(blob['x'], blob['y'], blob['width'], blob['height'], self.COLORS['lava'])

    def draw_enemies(self):
        """Draws the enemies."""
        for enemy in self.enemies:

            pyxel.rect(enemy['x'], enemy['y'], enemy['width'], enemy['height'], self.COLORS['enemy'])

    def draw(self):
        if self.game_state == "menu":
            self.draw_menu()
            return
        elif self.game_state == "complete":
            pyxel.cls(1)  # Dark blue background
            # Final time and high score display
            final_text = "FINAL TIME"
            final_time_text = self.format_time_ms(self.current_run_time_ms)
            label_x = (SCREEN_WIDTH // 2) - (len(final_text) * 4 // 2)
            value_x = (SCREEN_WIDTH // 2) - (len(final_time_text) * 4 // 2)
            pyxel.text(label_x, SCREEN_HEIGHT // 2 - 36, final_text, self.COLORS.get('level_exit', 11))
            pyxel.text(value_x, SCREEN_HEIGHT // 2 - 24, final_time_text, self.COLORS.get('player', 7))

            # Display death count
            deaths_text = f"Deaths: {self.death_count}"
            deaths_x = (SCREEN_WIDTH // 2) - (len(deaths_text) * 4 // 2)
            pyxel.text(deaths_x, SCREEN_HEIGHT // 2 - 12, deaths_text, 8)

            if self.highscore_ms is not None:
                hs_text = "BEST"
                hs_value = self.format_time_ms(self.highscore_ms)
                hs_label_x = (SCREEN_WIDTH // 2) - (len(hs_text) * 4 // 2)
                hs_value_x = (SCREEN_WIDTH // 2) - (len(hs_value) * 4 // 2)
                pyxel.text(hs_label_x, SCREEN_HEIGHT // 2 + 6, hs_text, self.COLORS.get('jump_pad', 10))
                pyxel.text(hs_value_x, SCREEN_HEIGHT // 2 + 16, hs_value, self.COLORS.get('jump_pad', 10))
                
            prompt = "Press R to return to menu"
            prompt_x = (SCREEN_WIDTH // 2) - (len(prompt) * 4 // 2)
            pyxel.text(prompt_x, SCREEN_HEIGHT - 20, prompt, self.COLORS.get('lava', 8))
            return

        pyxel.camera(self.player_x - SCREEN_WIDTH / 2, self.player_y - SCREEN_HEIGHT / 2)

        pyxel.cls(self.COLORS['sky'])

        flash_on = (pyxel.frame_count // 5) % 2 == 0

        rotated_tile_coords = set()
        for zone in self.rotating_zones:
            for tile in zone.tiles:
                rotated_tile_coords.add((tile['orig_x'] // TILE_SIZE, tile['orig_y'] // TILE_SIZE))

        flashing_tile_coords = set()
        for fz in self.flashing_zones:
            map_width = len(self.level_map[0])
            map_height = len(self.level_map)

            start_col = max(0, int((fz.center_x - fz.radius) // TILE_SIZE))
            end_col = min(map_width, int((fz.center_x + fz.radius) // TILE_SIZE) + 1)
            start_row = max(0, int((fz.center_y - fz.radius) // TILE_SIZE))
            end_row = min(map_height, int((fz.center_y + fz.radius) // TILE_SIZE) + 1)

            for row_index in range(start_row, end_row):
                for col_index in range(start_col, end_col):
                    tile_center_x = col_index * TILE_SIZE + TILE_SIZE / 2
                    tile_center_y = row_index * TILE_SIZE + TILE_SIZE / 2

                    dist_sq = (tile_center_x - fz.center_x)**2 + (tile_center_y - fz.center_y)**2
                    if dist_sq < fz.radius**2:
                        flashing_tile_coords.add((col_index, row_index))

        for row_index, row in enumerate(self.level_map):
            for col_index, tile in enumerate(row):

                if (col_index, row_index) in rotated_tile_coords:
                    continue

                x = col_index * TILE_SIZE
                y = row_index * TILE_SIZE

                base_color = None
                is_solid_or_hazard = False

                if tile == '1':
                    base_color = self.COLORS['ground']
                    is_solid_or_hazard = True
                elif tile == 'S':
                    base_color = self.COLORS['spikes']
                    is_solid_or_hazard = True
                elif tile == 'J':
                    base_color = self.COLORS['jump_pad']
                elif tile == 'E':
                    base_color = self.COLORS['level_exit']
                elif tile == 'g':
                    base_color = self.COLORS['low_gravity_block']
                    is_solid_or_hazard = True
                elif tile == 'f':
                    base_color = self.COLORS['flashing_block']
                elif tile == 'r' or tile == ' ':
                    pass
                elif tile == 'i':
                    continue

                elif tile == 'R':
                    base_color = self.COLORS['key']
                elif tile == 'Z':

                    base_color = 11 if self.has_key else self.COLORS['door']
                    is_solid_or_hazard = True

                else:
                    continue

                color_to_draw = base_color
                is_flashing = (col_index, row_index) in flashing_tile_coords

                if is_flashing:

                    if is_solid_or_hazard or tile == 'R' or tile == 'Z':
                        if flash_on:
                            color_to_draw = 7
                        else:
                            color_to_draw = 0

                        pyxel.rect(x, y, TILE_SIZE, TILE_SIZE, color_to_draw)
                        continue

                    elif tile == ' ' or tile == 'r':
                        if flash_on:
                            color_to_draw = 7
                        else:
                            color_to_draw = 0

                        pyxel.rect(x, y, TILE_SIZE, TILE_SIZE, color_to_draw)
                        continue

                    elif tile == 'f':
                        color_to_draw = self.COLORS['flashing_block']

                if color_to_draw is not None:
                    pyxel.rect(x, y, TILE_SIZE, TILE_SIZE, color_to_draw)

                    if tile == 'R':

                        pyxel.rect(x + 2, y + 3, 4, 2, 0)
                        pyxel.rect(x + 3, y + 2, 2, 4, 0)

                    elif tile == 'Z':

                         if self.has_key:
                             pyxel.circ(x + 5, y + 5, 1, 0)
                         else:
                             pyxel.rect(x + 4, y + 4, 1, 3, 7)

        for zone in self.rotating_zones:
            for tile in zone.tiles:
                color = self.COLORS['ground']
                if tile['char'] == 'S':
                    color = self.COLORS['spikes']
                elif tile['char'] == 'r':
                    color = self.COLORS['rotating_block']

                pyxel.rect(tile['x'], tile['y'], TILE_SIZE, TILE_SIZE, color)

        self.draw_lava()

        for p in self.moving_platforms:
            pyxel.rect(p['x'], p['y'], p['width'], p['height'], self.COLORS['moving_platform'])

        for s in self.moving_spikes:
            pyxel.rect(s['x'], s['y'], s['width'], s['height'], self.COLORS['moving_spikes'])

        for k in self.moving_jump_pads:
            pyxel.rect(k['x'], k['y'], k['width'], k['height'], self.COLORS['moving_jump_pad'])

        for d in self.moving_exits:
            pyxel.rect(d['x'], d['y'], d['width'], d['height'], self.COLORS['moving_exit'])

        self.draw_enemies()

        pyxel.rect(self.player_x, self.player_y, PLAYER_WIDTH, PLAYER_HEIGHT, self.COLORS['player'])

        # HUD (camera reset)
        pyxel.camera(0, 0)
        pyxel.text(5, 25, "Left/Right/Up to Movement and Jump", 7)
        pyxel.text(5, 15, "Touch wall while jumping for Wall Jump",87)
    

        # Draw level title and status
        if self.current_level != "Complete":
            level_title = LEVEL_TITLES.get(self.current_level, "Unknown")
            pyxel.text(5, 5, f"Level {self.current_level}: {level_title}", 7)

            if self.is_rotating:
                 pyxel.text(5, 55, "Rotating! Don't Slip!", 8)
            elif any(abs(self.player_vel_y) < GRAVITY * 0.9 for _ in self.low_gravity_blocks):
                 pyxel.text(5, 55, "Low Gravity", 6)

            key_status_color = 10 if self.has_key else 8
            key_status_text = "Key Collected!" if self.has_key else "Key Needed."
            pyxel.text(SCREEN_WIDTH - 60, 5, key_status_text, key_status_color)

            for state in self.enemy_states:
                if state['enemy'] is None:
                    pyxel.text(5, 55, f"Enemy Respawning: {state['respawn_timer'] // 60 + 1}s", 8)
                    break

        else:
            pyxel.text(SCREEN_WIDTH/2 - 20, SCREEN_HEIGHT/2, "You Win!", 7)

        # Draw the run timer at the top center (small but readable)
        timer_text = self.format_time_ms(self.current_run_time_ms)
        text_width = len(timer_text) * 4
        x = (SCREEN_WIDTH // 2) - (text_width // 2)
        y = 4  # small margin from top
        pyxel.text(x, y, timer_text, self.COLORS.get('player', 7))

PlatformerGame()
sys.exit()

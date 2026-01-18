# You import all the IOs of your board
import board
import busio

# These are imports from the kmk library
from kmk.kmk_keyboard import KMKKeyboard
from kmk.scanners.matrix import MatrixScanner
from kmk.keys import KC
from kmk.modules.macros import Press, Release, Tap, Macros
from kmk.extensions.display import Display, TextEntry, ImageEntry
from kmk.extensions.display.ssd1306 import SSD1306
from kmk.modules.encoder import EncoderHandler
from kmk.modules.layers import Layers
import time


# This is the main instance of your keyboard
keyboard = KMKKeyboard()

# Add the macro extension
macros = Macros()
keyboard.modules.append(macros)

# Add encoder extension
encoder_handler = EncoderHandler()
keyboard.extensions.append(encoder_handler)

# Add layers extension
keyboard.modules.append(Layers())

# OLED stuff
i2c_bus = busio.I2C(board.SCL, board.SDA)

driver = SSD1306(
    i2c=i2c_bus,
    device_address=0x3C,
)

display = Display(
    # Mandatory:
    display=driver,
    # Optional:
    width=128, # screen size
    height=32, # screen size
)


display.entries = [
    TextEntry(text='Macropad v1 C:', x=0, y=0)
]

keyboard.extensions.append(display)



# Pins
keyboard.matrix = MatrixScanner(
    row_pins = (board.D10, board.D9, board.D8),
    col_pins = (board.D1, board.D2, board.D3),
    columns_to_anodes = True,
)

# Encoder Pins
encoder_handler.pins = (
    (board.D6, board.D7, board.D0,),
)

# Here you define the buttons corresponding to the pins
# Look here for keycodes: https://github.com/KMKfw/kmk_firmware/blob/main/docs/en/keycodes.md
# And here for macros: https://github.com/KMKfw/kmk_firmware/blob/main/docs/en/macros.md
keyboard.keymap = [
    [
        KC.A, KC.B, KC.C, # Default layer
        KC.D, KC.E, KC.F,
        KC.G, KC.H, KC.I,
    ],
    [
        KC.J, KC.K, KC.L, # Gaming layer
        KC.M, KC.N, KC.O,
        KC.P, KC.Q, KC.R,
    ],
    [
        KC.S, KC.T, KC.U, # Editing layer
        KC.V, KC.W, KC.X,
        KC.Y, KC.Z, KC.SPC,
    ]
]

# Encoder map (one tuple per encoder per layer: (CCW, CW, PRESS))
# Each layer entry is a tuple for each encoder; we have 1 encoder, so each
# layer contains a single-tuple followed by a trailing comma to form the
# per-encoder sequence.
encoder_handler.map = [
    ((KC.VOLU, KC.VOLD, KC.MUTE),),               # layer 0
    ((KC.VOLU, KC.VOLD, KC.MUTE),),               # layer 1
    ((KC.VOLU, KC.VOLD, KC.MUTE),),               # layer 2
]

# Armed double-click encoder behavior
# Double-press encoder button to "arm" layer-switching, rotate to pick candidate,
# press once to confirm. Rotations when unarmed fall back to default behavior.
encoder_handler._armed = False
encoder_handler._last_button_ms = 0
encoder_handler._armed_since_ms = 0
encoder_handler._candidate_layer = 0
encoder_handler._arm_timeout_ms = 5000
_DOUBLE_CLICK_MS = 400

def _now_ms():
    return int(time.monotonic() * 1000)

# Keep original handlers so we can call them when not armed. If the
# encoder module hasn't assigned handlers yet, use safe no-op lambdas.
_orig_on_move = encoder_handler.on_move_do or (lambda *a, **k: None)
_orig_on_button = encoder_handler.on_button_do or (lambda *a, **k: None)

def _update_oled_status():
    try:
        # second entry reserved for status; create if missing
        if len(display.entries) < 2:
            display.entries.append(TextEntry(text='', x=0, y=10))
        if encoder_handler._armed:
            display.entries[1].text = f'Armed → {encoder_handler._candidate_layer}'
        else:
            # show current active layer
            display.entries[1].text = f'Layer {keyboard.active_layers[0]}'
    except Exception:
        pass

def _custom_on_move(keyboard_obj, encoder_id, state):
    now = _now_ms()
    # Auto-disarm on timeout
    if encoder_handler._armed and (now - encoder_handler._armed_since_ms) > encoder_handler._arm_timeout_ms:
        encoder_handler._armed = False
        _update_oled_status()

    if encoder_handler._armed:
        # Rotate changes candidate layer only
        num_layers = len(keyboard_obj.keymap)
        if state['direction'] == -1:
            # CCW -> layer down
            encoder_handler._candidate_layer = (encoder_handler._candidate_layer - 1) % num_layers
        else:
            # CW -> layer up
            encoder_handler._candidate_layer = (encoder_handler._candidate_layer + 1) % num_layers
        _update_oled_status()
    else:
        # Not armed: fallback to original behavior
        try:
            _orig_on_move(keyboard_obj, encoder_id, state)
        except Exception:
            pass

def _custom_on_button(keyboard_obj, encoder_id, state):
    now = _now_ms()
    # Only handle press events (not releases)
    if state.get('is_pressed'):
        # Double-click detection to arm
        if (now - encoder_handler._last_button_ms) <= _DOUBLE_CLICK_MS:
            # Toggle arm
            encoder_handler._armed = True
            encoder_handler._armed_since_ms = now
            encoder_handler._candidate_layer = keyboard.active_layers[0]
            encoder_handler._last_button_ms = 0
            _update_oled_status()
            return
        # If currently armed, single press confirms candidate
        if encoder_handler._armed:
            # send TO to switch to candidate layer
            try:
                keyboard_obj.tap_key(KC.TO(encoder_handler._candidate_layer))
            except Exception:
                pass
            encoder_handler._armed = False
            encoder_handler._last_button_ms = 0
            _update_oled_status()
            return
        # otherwise record time for possible double-click
        encoder_handler._last_button_ms = now
    # For other cases, fallback to original handler
    try:
        _orig_on_button(keyboard_obj, encoder_id, state)
    except Exception:
        pass

# Attach custom handlers
encoder_handler.on_move_do = _custom_on_move
encoder_handler.on_button_do = _custom_on_button

# Start kmk!
if __name__ == '__main__':
    keyboard.go()
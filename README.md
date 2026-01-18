# Icebergs' Macropad
This is the repo for my first macropad creation!

My macropad has 9 keyboard switches in a matrix, an OLED screen and a Rotary encoder! I will use it for video editing, gaming, and just other usefull things on my computer!
## CAD Model
The whole macropad fits together with just 4 screws on the case.
<img width="1520" height="722" alt="Macropad_Assembly_Render" src="https://github.com/user-attachments/assets/59b6c4f7-347f-4cbd-b655-751cb2d03028" />


## Case
I designed this to just hold the PCB with no extra screws. I made 2 support columns underneath the PCB to hold it up at the right height, and it should fit snug with not much wiggle room.
Once I get the parts in real life, I can make the case better as I do not know the actual dimentions for the OLED screen.
<img width="1520" height="722" alt="Macropad_Case_Render" src="https://github.com/user-attachments/assets/8bd38a86-9b7a-4f70-be3a-e68486fde89c" />


## PCB
The PCB was designed with 9 switches, 9 diodes, the Seeed Studio XIAO RP2040, an EC11 Rotary encoder, a 128x32 OLED screen, and a nice silkscreen graphic! The mounting holes in it are for the future if I need to mount the PCB inside the case, but for now, I wont be using them :)

<img width="573" height="857" alt="Screenshot 2026-01-17 112326" src="https://github.com/user-attachments/assets/ba9ea18e-746c-4827-b354-0846617b7ec0" />

## The Schematic

<img width="1277" height="620" alt="Screenshot 2026-01-17 112855" src="https://github.com/user-attachments/assets/5157eacd-a971-41c2-ae2d-4006367ba559" />

## Software
The software was made with KMK.
I have most of the code complete, just need to change the buttons and OLED screen
- Currently the switches are just mapped to normal characters, when I get the macropad I will start thinking of what to map them to
### Here are some features I included:
- 3 keyboard layers (1 default, 1 gaming and 1 video editing) - As i said earlier, I only have them mapped to characters currently
- Encoder to switch the layer (double click encoder to enter 'layer switching mode' and then turn encoder clockwise to go to next layer, counter clockwise to go to previous layer, and click the encoder again to confirm)
- OLED screen - This currently only has some text... I will be editing this a lot when my macropad arrives
The software was probably my favourite part of making this macropad (along with PCB design)

## BOM
Finaly, all the parts I used.
- 9x Through-hole 1N4148 Diodes
- 9x MX-Style switches
- 1x EC11 Rotary encoder
- 1x 0.91 inch OLED display
- 9x Blank DSA keycaps
- 4x M3x16mm screws
- And I am *pretty* sure that the heatset inserts are needed... Please tell me? If they are: 4x M3x5mx4mm heatset inserts

#### I do not need the 3D printed case - I have a 3D printer at home

Thank you HackClub for giving us this awesome experience!

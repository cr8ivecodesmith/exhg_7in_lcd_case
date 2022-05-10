from pathlib import Path

from solid import (
    # Objects
    part,
    cube,
    cylinder,

    # Transformations
    rotate,
    translate,
    color,

    # Operations

    # Utils
    scad_render_to_file,
)


# ### Configuration ###
SCAD_OUT = f'{Path(__file__).stem}.scad'
FRAGMENTS = 32

SCREW_HOLE_Di = 3  # Screw hole diameter (M3)
SCREW_PIN_L = 12  # Screw pin length (M3x12)

PANEL_W = 165  # Panel total width
PANEL_H = 123  # Panel total height
PANEL_D = 14.5  # Panel total depth
PANEL_LCD_D = 7.5  # Panel lcd depth

BPANEL_D = 2  # Back panel depth
BPANEL_MOUNT_D = 4.5  # BP mount depth
BPANEL_MOUNT_Di = 5 + SCREW_HOLE_Di  # BP mount diameter

FPANEL_D = PANEL_LCD_D + 1  # Front panel depth
FPANEL_TOP_CLR = 9
FPANEL_BOT_CLR = 12
FPANEL_LR_SIDE = 5
FPANEL_TB_SIDE = 13


def draw_lcd_model():
    pcb = cube((PANEL_W, PANEL_D - PANEL_LCD_D, PANEL_H), False)
    pcb = translate((0, PANEL_LCD_D, 0))(pcb)
    pcb = color('midnightblue')(pcb)

    lcd_z = PANEL_H - FPANEL_TOP_CLR - FPANEL_BOT_CLR
    lcd = cube((PANEL_W, PANEL_LCD_D, lcd_z), False)
    lcd = translate((0, 0, FPANEL_BOT_CLR))(lcd)
    lcd = color('dimgray')(lcd)

    model = pcb + lcd

    return model


def draw_front_panel():
    width = PANEL_W + (FPANEL_LR_SIDE * 2)

    bot = color('salmon')(cube((width, FPANEL_D, FPANEL_TB_SIDE), False))
    top = translate((0, 0, PANEL_H - FPANEL_TOP_CLR))(bot)

    left = color('tomato')(cube((FPANEL_LR_SIDE, FPANEL_D, PANEL_H), False))
    right = translate((width - FPANEL_LR_SIDE, 0, 0))(left)

    panel = top + bot + left + right

    return panel


def draw_back_panel():
    width = PANEL_W
    top_h = 12
    bot_h = 52
    mid_w = 152
    mid_h = PANEL_H - (bot_h + top_h)
    mount_offset = BPANEL_MOUNT_Di / 2

    # Define back panels
    top = translate((0, 0, PANEL_H - top_h))(
        cube((width, BPANEL_D, top_h), False)
    )
    bot = cube((width, BPANEL_D, bot_h), False)
    mid = translate((0, 0, PANEL_H - top_h - mid_h))(
        cube((mid_w, BPANEL_D, mid_h), False)
    )

    # Define mounting holes
    mount_t = rotate(a=-90, v=(1, 0, 0))(
        cylinder(d=BPANEL_MOUNT_Di, h=BPANEL_MOUNT_D, center=False)
    )
    mount_tl = translate((
        mount_offset,
        0,
        (PANEL_H - BPANEL_MOUNT_Di) + mount_offset
    ))(mount_t)
    mount_tr = translate((
        (width - BPANEL_MOUNT_Di) + mount_offset,
        0,
        (PANEL_H - BPANEL_MOUNT_Di) + mount_offset
    ))(mount_t)

    mount_b = rotate(a=-90, v=(1, 0, 0))(
        cylinder(d=BPANEL_MOUNT_Di, h=BPANEL_MOUNT_D, center=False)
    )
    mount_bl = translate((
        mount_offset,
        0,
        mount_offset
    ))(mount_b)
    mount_br = translate((
        (width - BPANEL_MOUNT_Di) + mount_offset,
        0,
        mount_offset
    ))(mount_b)

    # Combine the parts
    panel = part()
    panel.add(top + bot + mid)
    panel = translate((0, BPANEL_MOUNT_D, 0))(panel)

    mount = part()
    mount.add(mount_tr + mount_tl)
    mount.add(mount_br + mount_bl)

    return panel + mount


def draw_screw_pins():
    pin_offset = SCREW_HOLE_Di / 2
    pin = translate((pin_offset, 0, pin_offset))(rotate(a=-90, v=(1, 0, 0))(
        cylinder(d=SCREW_HOLE_Di, h=SCREW_PIN_L)
    ))
    pin = color('purple')(pin)

    # Define positions based on left and top positions of the bottom
    # left corner of the pin
    bl_l, bl_t = 2, 3.5
    br_l, br_t = PANEL_W - 2.2 - SCREW_HOLE_Di, 3.5
    tl_l, tl_t = 2, PANEL_H - 2.3 - SCREW_HOLE_Di
    tr_l, tr_t = PANEL_W - 2.6 - SCREW_HOLE_Di, PANEL_H - 2.3 - SCREW_HOLE_Di

    # Draw the pins
    bl = translate((bl_l, 0, bl_t))(pin)
    br = translate((br_l, 0, br_t))(pin)
    tl = translate((tl_l, 0, tl_t))(pin)
    tr = translate((tr_l, 0, tr_t))(pin)

    # Define panel mount pins
    pin_dist = 10
    bot_pin = translate(((PANEL_W / 2) - pin_offset, 8, pin_dist))(pin)
    side_pin = translate((152 - pin_dist, 8, (PANEL_H / 2) - pin_offset))(pin)

    # Combine
    panel_pins = tl + tr + bl + br
    mount_pins = bot_pin + side_pin

    return panel_pins + mount_pins


def draw_screw_pin_test():
    """This is used to measure the position of the screw holes in the LCD

    """
    # Define the frame and the pin
    frame_offset = 6
    frame = cube((PANEL_W, 0.2, PANEL_H)) - \
        translate((frame_offset, 0, frame_offset))(
            cube((
                PANEL_W - frame_offset * 2, 0.2, PANEL_H - frame_offset * 2))
        )
    pin_offset = SCREW_HOLE_Di / 2
    pin = translate((pin_offset, 0, pin_offset))(rotate(a=-90, v=(1, 0, 0))(
        cylinder(d=SCREW_HOLE_Di, h=BPANEL_MOUNT_D)
    ))
    pin = color('purple')(pin)

    # Define positions based on left and top positions of the bottom
    # left corner of the pin
    bl_l, bl_t = 2, 3.5
    br_l, br_t = PANEL_W - 2.2 - SCREW_HOLE_Di, 3.5
    tl_l, tl_t = 2, PANEL_H - 2.3 - SCREW_HOLE_Di
    tr_l, tr_t = PANEL_W - 2.6 - SCREW_HOLE_Di, PANEL_H - 2.3 - SCREW_HOLE_Di

    # Draw the pins
    bl_pin = translate((bl_l, -BPANEL_MOUNT_D, bl_t))(pin)
    br_pin = translate((br_l, -BPANEL_MOUNT_D, br_t))(pin)
    tl_pin = translate((tl_l, -BPANEL_MOUNT_D, tl_t))(pin)
    tr_pin = translate((tr_l, -BPANEL_MOUNT_D, tr_t))(pin)

    return frame + bl_pin + br_pin + tl_pin + tr_pin


def draw_panel_mount():
    # Define stand mount
    hi = 15
    r2 = 8
    r1 = 8
    bot_stand_cut = color('red')(
        translate((0, -r1, 0))(cube((r1 * 2, r1, hi))))
    bot_stand = translate((r1, 0, 0))(cylinder(h=hi, r1=r1, r2=r2))
    bot_stand = bot_stand - bot_stand_cut
    bot_stand = translate((
        (PANEL_W / 2) - r1, BPANEL_MOUNT_D + 1, 0
    ))(bot_stand)

    # Define the pin hole
    screw_size = 6  # M5x8
    pin = color('red')(translate((
        (PANEL_W / 2), (BPANEL_MOUNT_D + BPANEL_D + 3), 0
    ))(cylinder(d=screw_size, h=8)))

    # bot_stand = translate(((width / 2), r1 / 2, 0))(bot_stand)
    return bot_stand - pin


def main():
    front_panel = draw_front_panel()
    back_panel = translate((
        FPANEL_LR_SIDE, (PANEL_D - BPANEL_MOUNT_D) + 1, 1))(draw_back_panel())

    # Draw the lcd model in the ideal position
    lcd_model = translate((FPANEL_LR_SIDE, 1, 1))(draw_lcd_model())

    # Draw a panel mount
    panel_mount = translate((
        FPANEL_LR_SIDE, (PANEL_D - BPANEL_MOUNT_D) + 1, 1
    ))(draw_panel_mount())

    # Draw to screw pins
    screw_pins = translate((
        FPANEL_LR_SIDE, BPANEL_MOUNT_D + 1, 1))(draw_screw_pins())

    # Draw screw pin test
    # screw_test = translate((
    #     FPANEL_LR_SIDE, PANEL_D + BPANEL_MOUNT_D, 1))(draw_screw_pin_test())
    # screw_test = draw_screw_pin_test()

    # return screw_test
    # return lcd_model + screw_test

    # return lcd_model + front_panel
    # return front_panel
    # return lcd_model + screw_pins
    # return back_panel + screw_pins
    # return front_panel + back_panel
    # return lcd_model + back_panel
    # return (lcd_model + front_panel + back_panel) + screw_pins
    # return (front_panel + back_panel) - screw_pins
    # return (back_panel) - screw_pins
    return (panel_mount) - screw_pins
    # return front_panel - screw_pins
    # return (front_panel + back_panel + panel_mount) - screw_pins


if __name__ == '__main__':
    scad_render_to_file(
        main(), filepath=SCAD_OUT, file_header=f'$fn = {FRAGMENTS};'
    )

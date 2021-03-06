################################################################### Qtile Config ################################################################################ 

from typing import List
from libqtile import bar, layout, widget, qtile
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal

## for mouse follow focus
from xcffib.xproto import EventMask

################################################################### General ##################################################################################### 
mod = "mod4"
terminal = "kitty"
browser = "google-chrome"

widget_defaults = dict(
    font="sans",
    fontsize=12,
    padding=10,
)
extension_defaults = widget_defaults.copy()

screens = [
    Screen(
        bottom=bar.Bar(
            [
                widget.CurrentLayout(),
                widget.GroupBox(),
                widget.Prompt(),
                widget.WindowName(),
                widget.Chord(
                    chords_colors={
                        "launch": ("#ff0000", "#ffffff"),
                    },
                    name_transform=lambda name: name.upper(),
                ),
                widget.TextBox("default config", name="default"),
                widget.TextBox("Press &lt;M-r&gt; to spawn", foreground="#d75f5f"),
                widget.Systray(),
                widget.Clock(format="%Y-%m-%d %a %I:%M %p"),
                widget.QuickExit(),
            ],
            24,
            border_width=[0, 0, 0, 0],  # Draw top and bottom borders
            border_color=["000000", "000000", "000000", "000000"]  # Borders are magenta
        ),
    ),
]

##################################################################### Rules ######################################################################################
dgroups_key_binder = None
dgroups_app_rules = []  # type: List
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
    ]
)
auto_fullscreen = False
focus_on_window_activation = False
reconfigure_screens = True
auto_minimize = True
wmname = "LG3D"

################################################################### Key Bindings ################################################################################ 
keys = [
    ## Qtile
    Key([mod], "q", lazy.window.kill(), desc="Kill focused window"),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    
    ## Aplications
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    Key([mod], "b", lazy.spawn(browser), desc="Launch Browser"),

    ## Window Focus 
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], 'Tab', lazy.next_screen(), desc='Next monitor'),
    
    ## Move Window
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),
    Key([mod], "space", lazy.layout.next(), desc="Move window focus to other window"),
    
    ## Resize Window
    Key([mod, "control"], "h", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key([mod, "control"], "l", lazy.layout.grow_right(), desc="Grow window to the right"),
    Key([mod, "control"], "j", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),

    ## Layout
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    Key([mod, "shift"], "Return", lazy.layout.toggle_split(), desc="Toggle between split and unsplit sides of stack",),
    Key([mod, "shift"], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "r", lazy.spawncmd(), desc="Spawn a command using a prompt widget"),
]

groups = [Group(i) for i in "123456789"]

for i in groups:
    keys.extend(
        [
            Key(
                [mod],
                i.name,
                lazy.group[i.name].toscreen(),
                desc="Switch to group {}".format(i.name),
            ),
            Key(
                [mod, "shift"],
                i.name,
                lazy.window.togroup(i.name, switch_group=True),
                desc="Switch to & move focused window to group {}".format(i.name),
            ),
        ]
    )


# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]
######################################################################## Layout ################################################################################ 

layouts = [
    layout.Columns(border_focus_stack=["#d75f5f", "#8f3d3d"], border_width=0),
    layout.Max(),
    # Try more layouts by unleashing below layouts.
    # layout.Stack(num_stacks=2),
    # layout.Bsp(),
    # layout.Matrix(),
    # layout.MonadTall(),
    # layout.MonadWide(),
    # layout.RatioTile(),
    # layout.Tile(),
    # layout.TreeTab(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
]

#################################################################### Focus Follows Mouse #######################################################################
# def mouse_move(qtile):
#     qtile.core._root.set_attribute(eventmask=(EventMask.StructureNotify
#                                             | EventMask.SubstructureNotify
#                                             | EventMask.SubstructureRedirect
#                                             | EventMask.EnterWindow
#                                             | EventMask.LeaveWindow
#                                             | EventMask.ButtonPress
#                                             | EventMask.PointerMotion))
#     def screen_change(event):
#         assert qtile is not None
#         if qtile.config.follow_mouse_focus and not qtile.config.cursor_warp:
#             if hasattr(event, "root_x") and hasattr(event, "root_y"):
#                 screen = qtile.find_screen(event.root_x, event.root_y)
#                 if screen:
#                     index_under_mouse = screen.index
#                     if index_under_mouse != qtile.current_screen.index:
#                         qtile.focus_screen(index_under_mouse, warp=False)
#         qtile.process_button_motion(event.event_x, event.event_y)
#     setattr(qtile.core, "handle_MotionNotify", screen_change)
#
# @hook.subscribe.startup_once
# def my_func_name():
#     mouse_move(qtile)

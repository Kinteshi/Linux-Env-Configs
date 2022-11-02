# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from libqtile import bar, layout, widget, hook
from libqtile.config import Click, Drag, Group, Key, Match, Screen, KeyChord
from libqtile.lazy import lazy
import subprocess
import os
# from libqtile.utils import guess_terminal

mod = "mod4"
terminal = 'terminator'

keys = [
    # A list of available commands that can be bound to keys can be found
    # at https://docs.qtile.org/en/latest/manual/config/lazy.html
    # Switch between windows
    Key([mod], "Left", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "Right", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "Down", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "Up", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(), desc="Move window focus to other window"),
    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "Left", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "shift"], "Right", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "shift"], "Down", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "Up", lazy.layout.shuffle_up(), desc="Move window up"),
    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "Left", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key([mod, "control"], "Right", lazy.layout.grow_right(), desc="Grow window to the right"),
    Key([mod, "control"], "Down", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "Up", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key(
        [mod, "shift"],
        "Return",
        lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack",
    ),
    Key([mod], "Return", lazy.spawn('rofi -show drun -kb-cancel'), desc="Launch rofi"),
    Key([mod], "t", lazy.spawn(terminal), desc="Launch terminal"),
    # Toggle between different layouts as defined below
    Key([mod], "apostrophe", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "q", lazy.window.kill(), desc="Kill focused window"),
    Key([mod, "shift"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "shift"], "e", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod], "r", lazy.spawncmd(), desc="Spawn a command using a prompt widget"),
    # Power menu
    KeyChord([mod], 'BackSpace', [
        # Lock screen
        Key([], "l", lazy.spawn("i3lock -c 000000")),
        # Logout
        Key([], "e", lazy.shutdown()),
        # Suspend
        Key([], "s", lazy.spawn("i3lock && systemctl suspend")),
        # Hibernate
        Key([], "h", lazy.spawn("i3lock && systemctl hibernate")),
        # Reboot
        Key([], "r", lazy.spawn("systemctl reboot")),
        # Shutdown
        Key(['Control'], "s", lazy.spawn("systemctl poweroff")),
    ], mode=False, name='(l) lock, (e) logout, (s) suspend, (h) hibernate, (r) reboot, (CTRL+s) shutdown'),
    # Open .config/
    Key([mod], 'i', lazy.spawn(f'code {os.path.expanduser("~/.config/")}')),
    # Flameshot
    Key([mod, 'shift'], 's', lazy.spawn('flameshot gui')),
    # Thunar
    Key([mod], 'e', lazy.spawn('thunar')),
    # Volume
    Key([], 'XF86AudioRaiseVolume', lazy.spawn('pactl set-sink-volume @DEFAULT_SINK@ +5%')),
    Key([], 'XF86AudioLowerVolume', lazy.spawn('pactl set-sink-volume @DEFAULT_SINK@ -5%')),
    Key([], 'XF86AudioMute', lazy.spawn('pactl set-sink-mute @DEFAULT_SINK@ toggle')),
    # Switch between monitors
    Key([mod], 'period', lazy.next_screen()),
    # Bring back from floating
    Key([mod], 'f', lazy.window.toggle_floating()),
    # pavucontrol
    Key([mod], 'v', lazy.spawn('pavucontrol')),
]

groups = [Group(i) for i in "123456789"]

for i in groups:
    keys.extend(
        [
            # mod1 + letter of group = switch to group
            Key(
                [mod],
                i.name,
                lazy.group[i.name].toscreen(toggle=True),
                desc="Switch to group {}".format(i.name),
            ),
            # mod1 + shift + letter of group = switch to & move focused window to group
            Key(
                [mod, "shift"],
                i.name,
                lazy.window.togroup(i.name, switch_group=False),
                desc="Switch to & move focused window to group {}".format(i.name),
            ),
            # Or, use below if you prefer not to switch to that group.
            # # mod1 + shift + letter of group = move focused window to group
            # Key([mod, "shift"], i.name, lazy.window.togroup(i.name),
            #     desc="move focused window to group {}".format(i.name)),
        ]
    )

layouts = [
    layout.Columns(
        border_focus='#6272A4',
        border_focus_stack='#6272A4', 
        border_normal='#44475A',
        border_normal_stack='#44475A',
        border_width=2,
        margin=1,
        margin_on_single=0,
        ),
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

widget_defaults = dict(
    # font="Segoe UI",
    font='Cascadia Code',
    fontsize=14,
    padding=3,
)
extension_defaults = widget_defaults.copy()


# Widgets
chord = widget.Chord(
                    # chords_colors={
                    #     "launch": ("#ff0000", "#ffffff"),
                    # },
                    # name_transform=lambda name: name.upper(),
                )
notify = widget.Notify(action=False)
sep = widget.Sep()
# wlan = widget.Wlan()
battery = widget.Battery()
cpu = widget.CPU()
mem = widget.Memory(measure_mem='G', format='Mem: {MemUsed:.2f}G/{MemTotal:.2f}G')
clock = widget.Clock(format="%d/%m/%Y %a %H:%M:%S")
systray = widget.Systray()
quick_exit = widget.QuickExit()
check_updates = widget.CheckUpdates(distro='Arch_yay', update_interval=3600, initial_text='Checking for updates...', display_format='Updates: {updates}', colour_have_updates='#ff0000', colour_no_updates='#00ff00')

# Screens

# Autostart
@hook.subscribe.startup
def autostart():
    subprocess.Popen([os.path.expanduser('~/.config/screenlayout.sh')])
    subprocess.Popen(['feh', '--bg-fill', os.path.expanduser('~/.config/qtile/wallpapers/default.jpg')])


@hook.subscribe.startup_once
def autostart_once():
    subprocess.Popen(['nm-applet'])
    # subprocess.Popen(['picom', '--experimental-backends', '--config', os.path.expanduser('~/.config/picom/picom.conf')])
    subprocess.Popen(['blueman-applet'])
    # subprocess.Popen(['cbatticon'])


screens = [
    Screen(
        top=bar.Bar(
            [   
                widget.CurrentLayoutIcon(),
                widget.CurrentScreen(active_text='|', inactive_text='|'),
                widget.GroupBox(disable_drag=True, hide_unused=True),
                sep,
                widget.WindowName(),
                # notify,
                # sep,
                # widget.OpenWeather(
                #     location='Anapolis',
                # ),
                # sep,
                # wlan,
                # sep,
                battery,
                chord,
                # widget.DF(),
                sep,
                systray,
                sep,
                cpu,
                sep,
                mem,
                # check_updates,
                sep,
                clock,
                sep,
            ],
            24,
            # border_width=[2, 0, 2, 0],  # Draw top and bottom borders
            # border_color=["ff00ff", "000000", "ff00ff", "000000"]  # Borders are magenta
        ),
    ),
    Screen(
        top=bar.Bar(
            [   
                widget.CurrentLayoutIcon(),
                widget.CurrentScreen(active_text='|', inactive_text='|'),
                widget.GroupBox(disable_drag=True, hide_unused=True),
                sep,
                widget.WindowName(),
                # chord,
                # sep,
                # wlan,
                # sep,
                # battery,
                sep,
                cpu,
                sep,
                mem,
                sep,
                clock,
                sep,
            ],
            24,
        ),
    ),
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
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
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"

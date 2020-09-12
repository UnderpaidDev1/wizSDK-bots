import os

from wizsdk.utils import get_all_wiz_handles, XYZYaw
from wizsdk.keyboard import Keyboard
from wizsdk import Card

import subprocess
import asyncio
import time


async def launch_w101(username, password):
    initial_handles = set(get_all_wiz_handles())
    initial_handles_l = len(initial_handles)

    print(f"Launching w101 window for user {username}")

    subprocess.Popen(
        'cd "C:\ProgramData\KingsIsle Entertainment\Wizard101\Bin" && start WizardGraphicalClient.exe -L login.us.wizard101.com 12000',
        shell=True,
    )

    handles = get_all_wiz_handles()
    while len(handles) != initial_handles_l + 1:
        await asyncio.sleep(0.5)
        handles = get_all_wiz_handles()

    # Pop() to get first handle from set
    handle = set(handles).difference(initial_handles).pop()

    k = Keyboard(handle)
    k.type_string(username)
    k.type_key("\t")
    k.type_string(password)
    k.type_keycode(13)
    return handle


async def logout_and_in(player, confirm=False):
    print("Loging out")
    await player.send_key("ESC", 0.1)
    await player.mouse.click(259, 506)
    if confirm:
        await player.mouse.click(415, 415)
    # wait for player select screen
    print("Wait for loading")
    while not (player.pixel_matches_color((361, 599), (133, 36, 62), tolerance=20)):
        await player.wait(0.5)

    print("Log back in")
    await player.mouse.click(395, 594)
    await player.finish_loading()
    # if (player.is_crown_shop()):
    #     player.wait(0.5).press_key('esc').press_key('esc')


def is_first_char(player):
    return player.pixel_matches_color((223, 554), (20, 86, 154), 20)


def is_char_menu(player):
    return player.pixel_matches_color((361, 599), (133, 36, 62), tolerance=20)


async def finish_loading(player):
    print("Awaiting loading")
    while player.is_idle():
        await asyncio.sleep(0.2)

    while not player.is_idle():
        await asyncio.sleep(0.5)

    await asyncio.sleep(1)


async def create_character(player):
    for i in range(12):
        # Skip dialog
        await player.mouse.click(546, 610, duration=0.1, delay=0.1)

    # Skip the test
    await player.mouse.click(210, 540)
    # Select life school
    await player.mouse.click(444, 280, delay=0.5)
    # OK
    await player.mouse.click(621, 540, delay=0.1)
    # Next
    await player.mouse.click(546, 610, delay=0.1)
    # Next (far right)
    await player.mouse.click(747, 590, delay=0.1)
    # Next
    await player.mouse.click(546, 610, delay=0.1)
    # Done
    await player.mouse.click(624, 610, delay=0.1)


def kill_w101():
    os.system("taskkill /f /im  WizardGraphicalClient.exe")


async def fight_mob(player, name=None):
    while player.is_idle():
        quest = await player.walker.quest_xyz()
        await player.walk_to(quest)
        await player.send_key("W", 0.5)
        await player.wait(1)

    # Get a battle object from the player
    battle = player.get_battle(name)

    # Wait for the battle to have started
    await battle.start()

    while battle.in_progress:
        enemies = battle.get_enemy_pos()

        for enemy_pos, is_enemy in enumerate(enemies):
            if is_enemy:
                # Cast spell until spell goes through
                print(f"Attacking enemy {enemy_pos + 1}")
                i = 0
                while battle.is_turn():
                    # Select spell near center of deck
                    x_pos = 391 + (i * 26)
                    random_spell = Card(player, "random", x_pos)
                    # Click enemy
                    await random_spell.cast(target=enemy_pos)
                    await player.wait(0.5)
                    i += 1
                break

        await battle.next_turn()

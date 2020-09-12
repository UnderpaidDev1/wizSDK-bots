# from wizsdk import Client, unregister_all
from helpers import *
from location_constants import *
import traceback
import asyncio
import os
import sys

from wizsdk import Client, unregister_all
from wizsdk.utils import finish_all_loading

player = None


async def skip_tutorial(username, password):
    global player
    """
    Goes throught the "create wizard" dialog if needed.
    Skips the tutorial and selects the player
    """
    player_handle = await launch_w101(username, password)
    player = Client.register(handle=player_handle, name=username)

    await asyncio.sleep(6)
    await player.send_key("ENTER", 0.1)

    while (not is_first_char(player)) and (not is_char_menu(player)):
        await player.wait(0.5)

    if is_first_char(player):
        await create_character(player)
        await player.wait(2)

    await player.send_key("ENTER", 0.1)
    # Wait health globe to be visible
    while not (player.pixel_matches_color((26, 535), (240, 57, 83), tolerance=20)):
        await player.wait(1)

    # Kill window to skip tutorial
    kill_w101()
    player_handle = await launch_w101(username, password)
    player = Client.register(handle=player_handle, name=username)

    await asyncio.sleep(6)
    await player.send_key("ENTER", 0.1)

    while not is_char_menu(player):
        await player.wait(0.5)

    await player.wait(2)
    await player.send_key("ENTER", 0.1)
    # Wait health globe to be visible
    while not (player.pixel_matches_color((26, 535), (240, 57, 83), tolerance=40)):
        print("waiting")
        await player.wait(1)

    await player.mouse.click(624, 610)
    # Skip tutorial
    await player.mouse.click(312, 610)
    # Confirm yes
    await player.mouse.click(407, 376, delay=0.5)
    await player.finish_loading()

    await player.activate_hooks("player_struct", "quest_struct")
    print("Hooked")
    # Make sure the player_struct hook was called
    await player.send_key("W", 0.1)


async def level_1():
    global player
    # Ambrose
    await player.walk_to(L_AMBROSE)
    await player.go_through_dialog()

    # Transported to unicorn way
    await player.finish_loading()
    await player.go_through_dialog(2)
    await logout_and_in(player)
    await player.send_key("W", 0.1)

    # Private Connelly
    await player.walk_to(L_CONNELLY)
    await player.go_through_dialog(2)

    # Fight 2 lost souls
    await player.teleport_to(L_LOSTSOULS)
    await player.wait(2)
    for i in range(2):
        await fight_mob(player, "Lost Souls")
        if player.is_dialog_more():
            break

    await player.go_through_dialog()

    # Private Connelly
    await player.teleport_to(L_CONNELLY)
    await player.go_through_dialog(2)
    print("Level 1 complete!\n")


async def level_2():
    global player

    # CEREN NIGHTCHANT
    await player.walk_to(L_NIGHTCHANT)
    await player.go_through_dialog(2)

    # Fight 2 Pirates
    await player.teleport_to(L_PIRATES)
    await player.wait(2)
    for i in range(2):
        await fight_mob(player, "Pirates")
        if player.is_dialog_more():
            break

    await player.go_through_dialog()

    # CEREN NIGHTCHANT
    await player.teleport_to(L_NIGHTCHANT)
    await player.go_through_dialog(2)
    print("Level 2 complete!\n")


async def level_3():
    global player
    # Teleport to Hedge maze entrance
    await player.teleport_to(L_HEDGEMAZE)
    await player.send_key("W", 0.2)
    await player.finish_loading()

    await player.send_key("W", 1)
    await player.go_through_dialog()
    await player.walk_to(L_ORIEL)
    await player.go_through_dialog(2)

    # Exit hedgemaze
    await player.teleport_to(L_HEDGEMAZE_EXIT)
    await player.send_key("W", 0.2)
    await player.finish_loading()

    # Open the cages
    for cage in L_CAGES:
        await player.teleport_to(cage)
        while not player.is_press_x():
            await player.wait(0.5)

        await player.send_key("X", 0.1)
        await player.wait(1)

    # Fight fairies
    await player.teleport_to(L_FAIRIES)
    await player.wait(2)
    for i in range(2):
        await fight_mob(player, "Fairies")
        await player.send_key("SPACEBAR", 0.1)

    # Go back to hedgemaze
    await player.teleport_to(L_HEDGEMAZE)
    await player.send_key("W", 0.1)
    await player.finish_loading()

    # Walk until the Fairy dialog
    await player.send_key("W", 1)
    await player.go_through_dialog(2)

    # Wait for pesky animation
    await asyncio.sleep(1)

    # Go to lady oriel
    await player.walk_to(L_ORIEL)
    await player.go_through_dialog(2)
    print("Level 3 complete!\n")


async def level_4():
    global player
    # Exit hedgemaze
    await player.teleport_to(L_HEDGEMAZE_EXIT)
    await player.send_key("W", 0.2)
    await player.finish_loading()

    # Teleport to Ceren
    await player.teleport_to(L_NIGHTCHANT)
    await player.go_through_dialog(2)

    # Mark location
    await player.mouse.click(676, 584, delay=0.3)

    # Teleport to rattlebones
    await player.teleport_to(L_RATTLEBONES)
    await player.finish_loading()
    await player.send_key("W", 1)
    await player.go_through_dialog()
    # Fight
    await player.send_key("W", 1)
    await fight_mob(player, "Rattlebones")
    await player.go_through_dialog()
    # Go to marked location
    await player.mouse.click(699, 569, delay=0.3)
    await player.finish_loading()

    # Talk to ceren
    await player.go_through_dialog(4)

    # Go to the commons
    await player.mouse.click(628, 567, delay=0.3)
    await player.finish_loading()

    # Enter library
    await player.teleport_to(L_LIBRARY)
    await player.send_key("W", 0.2)
    await player.finish_loading()

    # Talk to Harold
    await player.walk_to(L_HAROLD)
    await player.go_through_dialog()
    # exit
    await player.send_key("S", 1.5)
    await player.finish_loading()

    # Enter Ambrose's office
    await player.teleport_to(L_OFFICE)
    await player.send_key("W", 0.2)
    await player.finish_loading()

    # Talk to Ambrose
    await player.walk_to(L_AMBROSE)
    await player.go_through_dialog(2)
    print("Level 4 complete\n")


async def level_up(username, password):
    global player
    """
    # TEST ONLY
    # await launch_w101(username, password)
    player = Client.register(name=username)
    # await player.finish_loading()
    await player.activate_hooks("player_struct", "quest_struct")
    # # Make sure character_hook has been called
    await player.send_key("W", 0.1)
    """

    await skip_tutorial(username, password)
    await level_1()
    await level_2()
    await level_3()
    await level_4()


def get_account():
    try:
        selected_account = False
        with open("accounts.txt", "r+") as file:
            accounts = file.read().split("\n")
            if len(accounts) > 0:
                selected_account = accounts.pop()
                file.seek(0)
                file.write("\n".join(accounts))
                file.truncate()

        print(selected_account)
        return selected_account

    except IOError:
        print("Unable to find accounts.txt file")
        return False

    return False


def set_completed(account):
    with open("completed.txt", "a") as file:
        file.write(account + "\n")


async def run_from_file():
    while True:
        # Get first account from file
        account = get_account()

        # Exit loop when no accounts are left
        if not account:
            break
        # Extract username and password
        username, password = [s.strip() for s in account.split(":")]
        await level_up(username, password)

        # Set as completed
        set_completed(account)


async def run_from_argv():
    try:
        acc_i = sys.argv.index("--single")
        account = sys.argv[acc_i + 1]
    except IndexError:
        print(f"Invalid number or arguments or invalid order")
        return 1

    username, password = account.split(":")
    await level_up(username, password)


async def run():
    try:
        if "--single" in sys.argv:
            await run_from_argv()
        else:
            await run_from_file()

    except Exception as e:
        traceback.print_exc()
    finally:
        """
        IMPORTANT!
        """
        await unregister_all()


asyncio.run(run())

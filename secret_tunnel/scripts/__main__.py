# Native imports
import os
import traceback

# Third party imports
import asyncio
from wizsdk import 
    Client, 
    unregister_all,
    register_windows, 
    XYZYaw

# Constants
L_FIGHT1 = XYZYaw(x=1085.361, y=-2914.182, z=0.195, yaw=5.417)
L_FIGHT2 = XYZYaw(x=5843.989, y=-4009.693, z=0.195, yaw=4.662) 

async def main():
    p1 = Client.register(name="Player1")
    await p1.activate_hooks()

    async def fight(name):
        battle = p1.get_battle(name)
        while await battle():
            temp = await p1.find_spell("tempest")
            epic = await p1.find_spell("epic")
            e_temp = await p1.find_spell("tempest-enchanted")
            if e_temp:
                await e_temp.cast()
            elif temp and epic:
                e_temp = await epic.enchant(temp)
                await e_temp.cast()
            else:
                await p1.pass_turn()

    # LOOP INDEFINITELY
    while True:
        # GO IN
        await p1.send_key("X", 0.1)
        await p1.wait(5)
        await p1.finish_loading()

        await p1.send_key("W", 1)
        await p1.go_through_dialog()
        # FIRST FIGHT
        await p1.teleport_to(L_FIGHT1)
        await p1.send_key("W", 1)
        await fight("Gannon")
        await p1.go_through_dialog()
        # SECOND FIGHT
        await p1.teleport_to(L_FIGHT2)
        await p1.wait(4)
        await p1.go_through_dialog()
        await p1.send_key("W", 1)
        await fight("Madd'n")

        # Start over
        await p1.go_through_dialog()
        await p1.logout_and_in(confirm=True)

# Error handling
async def run():
  try:
    await main()
  except Exception:
    traceback.print_exc()
  finally:
    await unregister_all()
    

# Start the thread
if __name__ == "__main__":
    asyncio.run(run())
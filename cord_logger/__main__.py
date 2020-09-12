from wizsdk import Client, XYZYaw, unregister_all
import asyncio
import os
import traceback

def to_fixed_3(f):
  return round(f * 1000) / 1000

async def print_coords():
  player = Client.register(name="COORD BOT")
  await player.activate_hooks("player_struct")
  # A cautious step to make sure the hook was called
  await player.send_key('W', .1)
  
  while True:
    print("Print XYZYaw")
    input("Press enter to print...")
    
    xyz = await player.walker.xyz()
    yaw = await player.walker.yaw()
    
    v = [to_fixed_3(n) for n in [*xyz, yaw]]
    
    print(XYZYaw(*v), '\n\n')

async def run():
  try:
    await print_coords()
  except Exception:
    traceback.print_exc()
  finally:
    # IMPORTANT
    await unregister_all()
    
asyncio.run(run())
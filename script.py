import math
import asyncio
import time

async def main():
    EX = 5
    
    print("--- Starting Loop ---")
    
    while True:
        # Set TIME to current system time
        TIME = time.time()
        
        # Calculate SIZE using math.cos
        # We use math.cos(5 * TIME) + EX
        SIZE = math.cos(5 * TIME) + EX
        
        print(f"Time: {TIME:.2f} | Size: {SIZE:.4f}")
        
        # Pause for 1 second so we don't spam the terminal too fast
        # Using asyncio.sleep allows the browser to stay responsive
        await asyncio.sleep(1)

# Run the async loop
asyncio.ensure_future(main())


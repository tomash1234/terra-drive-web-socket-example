import asyncio
import json
import websockets

HOST = "localhost"
PORT = 8765

async def handler(ws):
    async for msg in ws:
        print(msg)
        data = json.loads(msg)
        print("Received Data:", data)
        # Add your code here

async def main():
    async with websockets.serve(handler, HOST, PORT):
        await asyncio.Future()

if __name__ == '__main__':
    asyncio.run(main())


"""
Usage:

1. Start this script
2. Go to www.terradrive.eu and start the open world game
3. Press "`" or ";" key to open console
4. Type `/wsConnect localhost:8765`
5. You should start receiving game data
6. Check readme for info about data
7. Optional, stop sending data /wsDisconnect

"""
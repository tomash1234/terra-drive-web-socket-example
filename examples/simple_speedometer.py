import asyncio
import json
import math

import websockets
import threading
import tkinter as tk

HOST = "localhost"
PORT = 8765


class Gauge(tk.Canvas):
    def __init__(self, master, size=300, max_value=200, tick=20, bg="#202020", **kwargs):
        super().__init__(master, width=size, height=size, bg=bg, highlightthickness=0, **kwargs)
        self.size = size
        self.bg = bg
        self.max_value = max_value
        self.tick = tick
        self.center = size // 2
        self.radius = size * 0.4

        self.arrow = None

        self.draw_gauge()
        self.set_value(0)
        self.extra_value = None

    def draw_gauge(self):
        c = self.center
        r = self.radius

        self.create_oval(c - r, c - r, c + r, c + r, width=3, fill=self.bg, outline='#A0A0A0')

        for i in range(0, self.max_value + 1, self.tick):
            angle = self.value_to_angle(i)
            x1, y1 = self.polar(c, c, r * 0.9, angle)
            x2, y2 = self.polar(c, c, r * 1.0, angle)
            self.create_line(x1, y1, x2, y2, width=2, fill='white')

            xt, yt = self.polar(c, c, r * 0.75, angle)
            self.create_text(xt, yt, text=str(i), font=("Consolas", 10), fill='white')

    def value_to_angle(self, speed):
        return math.radians(-240 + 240 * (speed / self.max_value))

    def polar(self, cx, cy, r, angle):
        return cx + r * math.cos(angle), cy + r * math.sin(angle)

    def set_value(self, value):
        value = max(0, min(self.max_value, value))

        angle = self.value_to_angle(value)
        x, y = self.polar(self.center, self.center, self.radius * 0.85, angle)

        if self.arrow:
            self.delete(self.arrow)

        self.arrow = self.create_line(
            self.center, self.center, x, y,
            width=4, fill="red", arrow=tk.LAST
        )

    def set_extra_value(self, value):
        if self.extra_value:
            self.delete(self.extra_value)

        self.extra_value = self.create_text(self.center + self.radius / 3,
                                            self.center + self.radius / 2, text=value,
                                            font=("Consolas", 15), fill='white')


class WebSocketServer:

    def __init__(self, stop_event: threading.Event):
        self.state = {}
        self.stop_event = stop_event

    async def handler(self, ws):
        async for msg in ws:
            self.state = json.loads(msg)

    async def ws_server(self):
        async with websockets.serve(self.handler, HOST, PORT):
            while not self.stop_event.is_set():
                await asyncio.sleep(0.1)


def gear_str(value: int):
    if value == 0:
        return "R"
    elif value == 1:
        return "N"
    return str(value - 1)


def gui_loop(ws: WebSocketServer, stop_event: threading.Event):
    BACKGROUND_COLOR = "#202020"
    root = tk.Tk()
    root.title("TerraDrive Demo")
    frame = tk.Frame(root, bg=BACKGROUND_COLOR)
    frame.pack()

    speedo = Gauge(frame, size=300, max_value=180, background=BACKGROUND_COLOR)
    rpm = Gauge(frame, size=300, max_value=8, background=BACKGROUND_COLOR, tick=1)
    rpm.grid(row=0, column=0, padx=10)
    speedo.grid(row=0, column=1, padx=10)

    label_pos = tk.Label(frame, font=("Consolas", 14), fg="white", bg=BACKGROUND_COLOR)
    label_pos.grid(row=1, column=0, padx=10)
    label_in_game_pos = tk.Label(frame, font=("Consolas", 14), fg="#B0B0B0", bg=BACKGROUND_COLOR)
    label_in_game_pos.grid(row=2, column=0, padx=10)
    label_nav_point = tk.Label(frame, font=("Consolas", 14), fg="#B0B0B0", bg=BACKGROUND_COLOR)
    label_nav_point.grid(row=3, column=0, padx=10)

    def update():
        speedo.set_value(abs(ws.state.get("speed", 0) * 3.6))
        rpm.set_value(ws.state.get("rpm", 0) / 1000)

        gear = ws.state.get("gear", 1)
        rpm.set_extra_value(gear_str(gear))

        fuel = ws.state.get("fuel", 0.5)
        speedo.set_extra_value(f"{fuel * 100:.0f}%")

        lat = ws.state.get("pos", {}).get("lat", 0)
        lon = ws.state.get("pos", {}).get("lon", 0)
        heading = ws.state.get("heading", 0)

        label_pos.config(text=f"Pos: {lat:.6f}° {lon:.6f}° Heading: {heading:.1f}°")
        in_game_pos = ws.state.get("inGamePos", [0, 0, 0])
        label_in_game_pos.config(text=f"In game pos: {in_game_pos[0]:.1f} {in_game_pos[1]:.1f} {in_game_pos[2]:.1f}")

        nav_point = ws.state.get("navPoint")
        if nav_point:
            label_nav_point.config(text=f"Navigate to: {nav_point['lat']:.6f}° {nav_point['lon']:.6f}°")
        else:
            label_nav_point.config(text="Navigate to: None")

        root.after(16, update)

    def on_close():
        stop_event.set()
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_close)

    update()
    root.mainloop()


def main():
    stop_event = threading.Event()
    server = WebSocketServer(stop_event)
    threading.Thread(target=gui_loop, args=[server, stop_event], daemon=True).start()
    asyncio.run(server.ws_server())


if __name__ == '__main__':
    main()

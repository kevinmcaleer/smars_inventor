from time import sleep
import network
from secret import ssid, password
from machine import Pin, WDT
import uasyncio as asyncio
import socket
from vl53l1x import VL53L1X
from inventor import Inventor2040W
import json

PINS_BREAKOUT_GARDEN = {"sda": 4, "scl": 5}
board = Inventor2040W()
i2c = board.i2c

sensor = VL53L1X(i2c)

onboard = Pin("LED", Pin.OUT, value=0)
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)

while wlan.isconnected() == False:
    print(".", end="")
    sleep(0.5)
print(wlan.ifconfig())

f = open("index.html","r")
html = f.read()
f.close()

distance = sensor.distance

async def serve_client(reader, writer):
    global sensor, html, distance
    sensor_reading = sensor.distance
    print("Client Connected")
    request_line = await reader.readline()
    print("Request:", request_line)
    while await reader.readline() != b"\r\n":
#         print("awaiting readline")
        pass
    
    request = str(request_line)
    print(request)
    url = request.find('/distance')
    percent = str(100 - (2600 // sensor_reading ))
    print(percent)
    if url == 6:
        distance = {'distance': sensor_reading //10, 'percent':percent}
        response = json.dumps(distance)
    else:
        response = html % (str(sensor_reading), percent)
    writer.write('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
    writer.write(response)
    
    await writer.drain()
    await writer.wait_closed()
    print('Client Disconnected')

async def main():
    global sensor
    
    print ("setting up webserver")
    asyncio.create_task(asyncio.start_server(serve_client, "0.0.0.0", 80))
#     wdt = WDT(timeout=8000)
    count = 0
    while True:
        #distance = sensor.distance
        distance = 0
        onboard.on()
        ip = wlan.ifconfig()
        count += 1
        print(f"heartbeat {count}, distance {distance}, IP: {ip[0]}")
#         wdt.feed()
        await asyncio.sleep(0.25)
        onboard.off()
        await asyncio.sleep(0.25)

try:
    asyncio.run(main())
finally:
    asyncio.new_event_loop()
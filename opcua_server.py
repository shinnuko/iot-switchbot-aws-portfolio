# =====================================
# OPC UA Server
# SwitchBotの温度・湿度・CO2を公開する
# =====================================

import asyncio
from asyncua import Server

from switchbot import get_device_status


DEVICE_ID = "B0E9FE5598ED"


async def main():
    server = Server()
    await server.init()

    server.set_endpoint("opc.tcp://0.0.0.0:4840/freeopcua/server/")
    server.set_server_name("IoT Portfolio OPC UA Server")

    uri = "https://iot-portfolio.local"
    idx = await server.register_namespace(uri)

    objects = server.nodes.objects
    sensor = await objects.add_object(idx, "SwitchBot")

    temperature = await sensor.add_variable(idx, "Temperature", 0.0)
    humidity = await sensor.add_variable(idx, "Humidity", 0)
    co2 = await sensor.add_variable(idx, "CO2", 0)
    battery = await sensor.add_variable(idx, "Battery", 0)

    await temperature.set_writable()
    await humidity.set_writable()
    await co2.set_writable()
    await battery.set_writable()

    print("=" * 40)
    print("OPC UA Server 起動")
    print("opc.tcp://localhost:4840/freeopcua/server/")
    print("=" * 40)

    async with server:
        while True:
            status = get_device_status(DEVICE_ID)
            body = status["body"]

            await temperature.write_value(float(body["temperature"]))
            await humidity.write_value(int(body["humidity"]))
            await co2.write_value(int(body["CO2"]))
            await battery.write_value(int(body["battery"]))

            print(
                f"更新: 温度={body['temperature']}℃, "
                f"湿度={body['humidity']}%, "
                f"CO2={body['CO2']}ppm, "
                f"電池={body['battery']}%"
            )

            await asyncio.sleep(10)


if __name__ == "__main__":
    asyncio.run(main())
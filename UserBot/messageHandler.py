from pyrogram import Client, filters

app = Client(f"sessions/donqhomo")

@app.on_message(filters.text)
async def echo(client, message):
    await print(message)

app.run()
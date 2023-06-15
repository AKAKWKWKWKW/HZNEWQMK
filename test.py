from telethon import TelegramClient

api_id = '2152647'
api_hash = '5fd09f7a92d896c677280284c2ba1cce'

client = TelegramClient(session='WAVE1', api_id=api_id, api_hash=api_hash, app_version='Version alpha', 
        device_model='Test models', system_version='Android 999')

client.start()

async def test():

    tt = await client.get_messages('me', limit=1)
    print(tt)

client.loop.run_until_complete(test())

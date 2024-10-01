from telethon.sync import TelegramClient
from telethon.tl.functions.channels import InviteToChannelRequest
from telethon.tl.types import InputPeerUser
from telethon.errors import FloodWaitError
import asyncio
import colorama
import random
import os

api_id = 20257810
api_hash = 'a59d61700d4a8962834e7ca8c3168bc3'
phone = '+13235546197'
client = TelegramClient(phone, api_id, api_hash)

async def adder():
    try:
        file_path = input("Enter file path with users: ")
        with open(file_path, 'r') as file:
            users = file.readlines()
        channel_url = input("Enter the Telegram channel URL: ")
        target_channel = await client.get_entity(channel_url)

        print(f'Channel: {target_channel.title}')
        
        for user in users:
            user = user.strip()
            userid, access_hash = map(int, user.split(','))

            try:
                user_to_add = InputPeerUser(user_id=userid, access_hash=access_hash)
                await client(InviteToChannelRequest(target_channel, [user_to_add]))
                print(f"User {userid} invited successfully.")
                await asyncio.sleep(random.randrange(30, 70))

            except FloodWaitError as e:
                print(f"Flood wait error. Sleeping for {e.seconds} seconds.")
                await asyncio.sleep(e.seconds)
            except Exception as invite_error:
                print(f"Failed to invite user {userid}: {invite_error}")
                await asyncio.sleep(random.randrange(40, 50))

    except Exception as e:
        print(f"An error occurred: {e}")

async def scraper():
    try:
        group_chats_file = input("Enter file path with groups URLs: ")
        with open(group_chats_file, 'r') as file:
            group_chats = file.readlines()

        for group_url in group_chats:
            group_url = group_url.strip()
            group = await client.get_entity(group_url)
            async for user in client.iter_participants(group):
                with open('users.txt', 'a') as output:
                    if user.id and user.access_hash:
                        output.write(f"{user.id},{user.access_hash}\n")
            print(f"Finished scraping group: {group.title}")

    except Exception as e:
        print(f"An error occurred: {e}")

async def main():
    try:
        await client.connect()
        if not await client.is_user_authorized():
            await client.send_code_request(phone)
            code = input('Enter the code you received: ')
            await client.sign_in(phone, code)

        print(f'''
         _      __      
        (_)    / _|     
        _ ___| |_ ___  
        | / __|  _/ _ \ 
        | \__ \ || (_) |
        |_|___/_| \___/ 
                        
        Telegram: @isfo21

        {colorama.Fore.GREEN} Select Mode:
        {colorama.Fore.LIGHTMAGENTA_EX} [1] Adder
        {colorama.Fore.YELLOW} [2] Scraper
        ''')
        mode = input(colorama.Fore.BLUE+"Select Mode: ")
        
        if mode == '1':
            await adder()
        elif mode == '2':
            await scraper()
        else:
            print("Invalid mode selected")

    except Exception as e:
        print(f"An error occurred: {e}")
    
    finally:
        await client.disconnect()

if __name__ == '__main__':
    asyncio.run(main())
# Telegram User Agent Bot

### Modulу architecture

```.sh
UserBot
├── __init__.py
├── Makefile
├── README.md
├── requirements.txt
└── TGUserAgent
    ├── database
    │   ├── Accounts.py
    │   ├── Channels.py
    │   ├── database.py
    │   ├── dbworker.py
    │   ├── __init__.py
    │   ├── Messages.py
    │   └── userbot.sqlite
    ├── downloads
    ├── __init__.py
    ├── messageHandler.py
    ├── sessions
    │   └── donqhomo.session
    └── UserBot.py

4 directories, 15 files

```
------------
### Implemented methods file: [Stattron/UserBot/TGUserAgent/UserBot.py](https://github.com/bubblesortdudoser/Stattron/blob/main/UserBot/TGUserAgent/UserBot.py)

### 1. Register new account 
```.py
    # Register new account!
    #----------------------
     register_account = create_account(
         api_id=os.getenv('api_id'),
         api_hash=os.getenv('api_hash'),
         phone="89162107493",
         username=os.getenv('username'),
         host="149.154.167.50",
         port=443,
         public_key="-----BEGIN RSA PUBLIC KEY-----MII <...> AB-----END RSA PUBLIC KEY-----"
    )
    print(register_account)
```
### 2. Get account from db
```.py
    # Get account from db
    # ----------------------
    get_account_res = get_account(username="donqhomo")
    print(get_account_res)

```

### 3. Create session for account in db
```.py
    # Create session for account in db
    # ----------------------
    res3 = init_session(username="donqhomo")
    print(res3)

```

### 4. Delete account from db
```.py
    # Delete account from db
    # ----------------------
    res4 = delete_account(username="donqhomo")
    print(res4)
```

### 5. Init User Agent Bot
```.py
# Init User Agent Bot
    # ----------------------
    if get_account_res['status']:
        ubot = UserBot(username=get_account_res['account'].username, debug=False)

        loop = asyncio.get_event_loop()
        run = loop.run_until_complete
```

### 6. Get channels of account
```.py
    # Get channels of account
    # ----------------------
        channels = run(ubot.get_channels(account = get_account_res['account'], category="category1"))
        for channel in channels:
            print(channel, "\n\n")
```

### 7. Download media from telegram
```.py
    # Download media from telegram
    # ----------------------
    download_media = run(ubot.download_media(file_id="AQADAgADxbAxGyB2GUoAEAMAA7R3peUW____9UWLTY68ItIABB4E"))
    print(download_media)
```

### 8. Join chat
```.py
    # Join chat
    # ----------------------
    join_chat = run(ubot.join_chat(chat_id = "@rozetked", account=get_account_res['account'], category="category2"))
    print(join_chat)
```

### 9. Members count
```.py
    # Members count (+update members_count)
    # ----------------------
    members_count = run(ubot.get_chat_members_count(chat_id=-1001007302005))
    print(members_count)
```

### 10. Leave chat
```.py
    # Leave chat
    # ----------------------
    res = run (ubot.leave_chat(chat_id=-1001007302005))
    print(res)
    leave_chat = delete_channel(channel_id=-1001007302005)
    print(leave_chat)
```

### 11. Get chat History | update average views(for all times) and er(for all times)
```.py
    # Get chat History | update average views(for all times) and er(for all times)
    # ----------------------
    chat_history, avg_views, er  = run(ubot.get_chat_history(chat_id=-1001301455979,account=get_account_res['account'], mentions=['donqhomo']))
    
    for res in chat_history:
        print(chat_history[res], '\n\n\n')
    
    print(avg_views)
    print(er)
```


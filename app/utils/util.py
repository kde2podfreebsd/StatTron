def representation_account(account):
    return {
        "api_id": account.api_id,
        "api_hash": account.api_hash,
        "phone": account.phone,
        "username": account.username,
        "host": account.host,
        "port": account.port,
        "public_key": account.public_key
    }

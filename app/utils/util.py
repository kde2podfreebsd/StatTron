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


def representation_channel(channel):
    return {
        "channel_id": channel.channel_id,
        "is_scam": channel.is_scam,
        "is_private": channel.is_private,
        "title": channel.title,
        "username": channel.username,
        "members_count": channel.members_count,
        "description": channel.description,
        "category": channel.category,
        "photo_big_file_id": channel.photo_big_file_id,
        "photo_small_file_id": channel.photo_small_file_id,
        "small_photo_path": channel.small_photo_path,
        "average_views": channel.average_views,
        "er_all": channel.er_all,
    }

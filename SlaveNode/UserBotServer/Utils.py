import datetime

def extractUsernameToIdDict(stored_channels):

    stored_channels_usernames = list(
        x.link.split("/")[-1] if x.link is not None else None
        for x in stored_channels
    )
    stored_channels_ids = list(x.id_channel for x in stored_channels)

    stored_channels = dict(
        zip(stored_channels_usernames, stored_channels_ids)
    )

    return stored_channels


def gotoDailyBackup(certainHour: int = 20,
                    certainMinuteFrom: int = 30,
                    certainMinuteTo: int = 40, now: datetime = datetime.datetime.now()):
    return now.hour == certainHour and now.minute > certainMinuteFrom and now.minute < certainMinuteTo

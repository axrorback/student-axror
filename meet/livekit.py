import os
from dotenv import load_dotenv
load_dotenv()
from livekit.api import AccessToken,VideoGrants

API_KEY = os.getenv('LIVEKIT_API_KEY')
API_SECRET = os.getenv('LIVEKIT_API_SECRET')


def create_room_token(room_name,identity,):
    token = (
        AccessToken(api_key=API_KEY,api_secret=API_SECRET).with_identity(identity).with_grants(
            VideoGrants(
                room_join=True,
                room=room_name,
                can_publish=True,
                can_subscribe=True,
                can_publish_sources=[
                    "camera",
                    "microphone",
                    "screen_share",
                    "screen_share_audio",
                ],
            )
        )
    )

    return token.to_jwt()
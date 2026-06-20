from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())

from livekit.api import AccessToken, VideoGrants

token = AccessToken(
    api_key="acharya",
    api_secret="587ed2dfed759980ec8125ec492ae155"
).with_grants(VideoGrants(
    room_join=True,
    room="test-room"
)).with_identity("user2").to_jwt()

print(token)
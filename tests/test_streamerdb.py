from streamerdb import Tortoise, Streamer, Username, ViewerlistAppearance, ChatMessage
import pytest


@pytest.mark.asyncio
async def test_streamerdb():
    await Tortoise.init(db_url="sqlite://:memory:", modules={"models": ["streamerdb"]})
    await Tortoise.generate_schemas()
    un = await Username.create(username="bob")
    st = await Streamer.create(username=un, platform='twitch')
    va = await ViewerlistAppearance.create(streamer=st, viewer=un)
    ch = await ChatMessage.create(streamer=st, viewer=un, message="Hello World")
    await Tortoise.close_connections()

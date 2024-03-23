"""Defines objects that represent users on Twitch"""
from tortoise.models import Model
from tortoise import fields, Tortoise


class TimestampedModel(Model):
    created = fields.DatetimeField(auto_now_add=True, description="Created datetime")
    modified = fields.DatetimeField(auto_now=True, description="Modified datetime")

    class Meta:
        abstract = True


class Username(TimestampedModel):
    id = fields.IntField(pk=True)
    username = fields.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.username

    def __repr__(self):
        return f"Username({self.username})"


class ViewerlistAppearance(TimestampedModel):
    id = fields.BigIntField(pk=True)
    viewer = fields.ForeignKeyField('models.Username', related_name='appearances')
    streamer = fields.ForeignKeyField('models.Username', related_name='viewer_appearances')
    when = fields.DatetimeField()

    def __str__(self):
        return f"ViewerlistAppearance({self.viewer}, {self.streamer}, {self.when})"

    def __repr__(self):
        return f"ViewerlistAppearance({self.viewer}, {self.streamer}, {self.when})"


class Streamer(TimestampedModel):
    id = fields.IntField(pk=True)
    username = fields.ForeignKeyField('models.Username', related_name='accounts', null=False)
    platform = fields.CharField(max_length=255, null=False)

    class Meta:
        unique_together = ('username', 'platform')

    def __str__(self):
        return f"Streamer({self.username}, {self.platform})"

    def __repr__(self):
        return f"Streamer({self.username}, {self.platform})"

    async def get_chat_url(self) -> str:
        if self.platform == 'twitch':
            return f'https://www.twitch.tv/{await self.username}/chat'
        raise NotImplementedError

    def get_stream_url(self) -> str:
        try:
            return {'twitch': f'https://www.twitch.tv/{self.username}',
                    'pomf': f'https://pomf.tv/stream/{self.username}'}[self.platform]
        except KeyError as e:
            raise NotImplemented from e


class ChatMessage(TimestampedModel):
    id = fields.BigIntField(pk=True)
    streamer = fields.ForeignKeyField('models.Streamer', related_name='chat_messages')
    viewer = fields.ForeignKeyField('models.Username', related_name='sent_messages')
    message = fields.TextField()

    def __str__(self):
        return f"ChatMessage({self.streamer}, {self.viewer}, {self.created}, {self.message})"

    def __repr__(self):
        return f"ChatMessage({self.streamer}, {self.viewer}, {self.created}, {self.message})"


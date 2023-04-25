from app import ma
from app.audio.model import *

class AudioSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Audio
        exclude = ('is_deleted',)
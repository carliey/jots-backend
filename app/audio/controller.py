from flask import Blueprint
from app.route_guard import auth_required

from app.audio.model import *
from app.audio.schema import *

bp = Blueprint('audio', __name__)

@bp.post('/audio')
@auth_required()
def create_audio():
    audio = Audio.create()
    return AudioSchema().dump(audio), 201

@bp.get('/audio/<int:id>')
@auth_required()
def get_audio(id):
    audio = Audio.get_by_id(id)
    if audio is None:
        return {'message': 'Audio not found'}, 404
    return AudioSchema().dump(audio), 200

@bp.patch('/audio/<int:id>')
@auth_required()
def update_audio(id):
    audio = Audio.get_by_id(id)
    if audio is None:
        return {'message': 'Audio not found'}, 404
    audio.update()
    return AudioSchema().dump(audio), 200

@bp.delete('/audio/<int:id>')
@auth_required()
def delete_audio(id):
    audio = Audio.get_by_id(id)
    if audio is None:
        return {'message': 'Audio not found'}, 404
    audio.delete()
    return {'message': 'Audio deleted successfully'}, 200

@bp.get('/audios')
@auth_required()
def get_audios():
    audios = Audio.get_all()
    return AudioSchema(many=True).dump(audios), 200
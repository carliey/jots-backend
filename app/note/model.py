from app import db
from helpers.elevenlabs import vocalize
from helpers.openai import chat, transcribe
from helpers.formater import clean, md2text
from helpers.upload import add
from app.audio.model import Audio

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    creator_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    subject = db.Column(db.String)
    topic = db.Column(db.String)
    level = db.Column(db.String)
    curriculum = db.Column(db.String)
    raw = db.Column(db.String)
    clean = db.Column(db.String)
    images = db.relationship('Image')
    audio = db.relationship('Audio')
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now())
    is_deleted = db.Column(db.Boolean, default=False)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self, subject=None, topic=None, level=None, curriculum=None, raw=None, clean=None):
        self.subject = subject or self.subject
        self.topic = topic or self.topic
        self.level = level or self.level
        self.curriculum = curriculum or self.curriculum
        self.raw = raw or self.raw
        self.clean = clean or self.clean
        self.updated_at = db.func.now()
        db.session.commit()
    
    def delete(self):
        self.is_deleted = True
        self.updated_at = db.func.now()
        db.session.commit()
    
    def update_image_prompt(self, old_prompt, new_prompt):
        self.raw.replace(f'[image: {old_prompt}]', f'[image: {new_prompt}]')
        self.updated_at = db.func.now()
        db.session.commit()

    def remove_image(self, image_id, prompt):
        self.raw.replace(f'[image: {prompt}]', '')
        self.clean.replace(f'[image:{image_id}]', '')
        self.updated_at = db.func.now()
        db.session.commit()

    @classmethod
    def get_by_id(cls, id):
        return cls.query.filter_by(id=id, is_deleted=False).first()
    
    @classmethod
    def get_all_by_creator_id(cls, creator_id):
        return cls.query.filter_by(is_deleted=False, creator_id=creator_id).all()
    
    @classmethod
    def create(cls, subject, topic, curriculum, level, creator_id):
        note = cls(subject=subject, topic=topic, curriculum=curriculum, level=level, creator_id=creator_id)
        note.save()
        request = f"""
            subject:{subject}
            topic:{topic}
            curriculum:{curriculum}
            level:{level}
            """
        raw = chat('note', request)
        note.update(raw=raw, clean=clean(raw, note.id))
        return note
    
    @classmethod
    def create_from_audio(cls, subject, topic, curriculum, level, creator_id, audio):
        """
        starts by storing the note meta data:
            subject
            topic
            curriculum
            level
            creator_id
        """
        note = cls(subject=subject, topic=topic, curriculum=curriculum, level=level, creator_id=creator_id)
        note.save()
        # Stores the original audio to the database
        original_audio_url = add(audio, '', 'file')
        Audio.create('original', original_audio_url, note.id)
        # Generates the audio transcript from whisper
        transcript = transcribe(audio)
        # prepare a prompt for GPT3 to get the raw note
        request = f"transcript:{transcript}"
        raw = chat('transcript', request)
        # Stores the generated audio  audio to the database
        if Audio.no_recent_audio():
            print('No recent audio found, creating...')
            generated_audio = vocalize(md2text(raw))
            generated_audio_url = add(generated_audio, '', 'bytes')
            Audio.create('generated', generated_audio_url, note.id)
        # stores the cleaned note to the database
        note.update(raw=raw, clean=clean(raw, note.id))
        return note
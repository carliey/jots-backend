from app import db
import datetime

class Audio(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    url = db.Column(db.String)
    note_id = db.Column(db.Integer, db.ForeignKey('note.id'))
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now())
    is_deleted = db.Column(db.Boolean, default=False)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self, name=None):
        self.name = name or self.name
        self.updated_at = db.func.now()
        db.session.commit()
    
    def delete(self):
        self.is_deleted = True
        self.updated_at = db.func.now()
        db.session.commit()

    @classmethod
    def get_by_id(cls, id):
        return cls.query.filter_by(id=id, is_deleted=False).first()
    
    @classmethod
    def get_all(cls):
        return cls.query.filter_by(is_deleted=False).all()
    
    @classmethod
    def create(cls, name, url, note_id):
        audio = cls(name=name, url=url, note_id=note_id)
        audio.save()
        return audio
    
    @classmethod
    def no_recent_audio(cls):
        """Return True if the last audio was created more than 10 hours ago."""
        last_created_at = cls.query.order_by(cls.created_at.desc()).first().created_at
        ten_hours_ago = datetime.datetime.now() - datetime.timedelta(hours=10)
        return last_created_at <= ten_hours_ago
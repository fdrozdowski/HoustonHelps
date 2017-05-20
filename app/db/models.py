from app import db


class CraigslistItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(256), index=True)
    category = db.Column(db.String(256), index=True)
    location = db.Column(db.PickleType())
    url = db.Column(db.String())
    image_url = db.Column(db.String())

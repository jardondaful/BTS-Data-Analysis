from db import db

class Artist(db.Model):
    id = db.Column(db.String(50), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    popularity = db.Column(db.Integer)
    followers = db.Column(db.Integer)
    genres = db.Column(db.String(250))

class Album(db.Model):
    id = db.Column(db.String(50), primary_key=True)
    artist_id = db.Column(db.String(50), db.ForeignKey('artist.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    release_date = db.Column(db.String(10))

class Track(db.Model):
    id = db.Column(db.String(50), primary_key=True)
    album_id = db.Column(db.String(50), db.ForeignKey('album.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    duration_ms = db.Column(db.Integer)
    popularity = db.Column(db.Integer)

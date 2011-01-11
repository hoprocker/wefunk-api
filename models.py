from google.appengine.ext import db

class Show(db.Model):
    number = db.IntegerProperty()
    date = db.DateProperty()
    credits = db.StringProperty()
    page_url = db.LinkProperty()
    audio_url = db.LinkProperty()
    img_url = db.LinkProperty()
    desc = db.TextProperty()
    playlist = db.ListProperty(db.Key, verbose_name="playlist tracks")
    mstotal = db.IntegerProperty()

class Track(db.Model):
    show = db.ReferenceProperty(Show)
    id_hash = db.StringProperty()
    artist = db.StringProperty()
    title = db.StringProperty()
    start_mspos = db.IntegerProperty()


from app import db


class Card(db.Model):
    card_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    message = db.Column(db.String)
    like_count = db.Column(db.Integer)
    board_id = db.Column(db.Integer, db.ForeignKey('board.board_id'), nullable=True)
    board = db.relationship("Board", back_populates="cards")

    def get_dict(self):
        return {
            'card_id': self.card_id,
            'message':  self.message,
            'like_count': self.like_count
        }

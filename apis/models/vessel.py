from apis.models.model import db
from flask import jsonify

class Vessel(db.Model):
    __tablename__ = 'vessels'

    id = db.Column(db.BigInteger, primary_key=True)
    code = db.Column(db.String(8), unique=True)

    def __init__(self, vessel_code: str):
            self.code = vessel_code

    def saveVessel(self):
        
        try:
            db.session.add(self)
            db.session.commit()
            return jsonify(id=self.id, code=self.code)
        except:
            return jsonify(message='Error while trying to save vessel')

    @classmethod
    def getVesselByCode(cls, vessel_code: str):
        vessel = cls.query.filter_by(code=vessel_code).first()
        if vessel:
            return vessel
        return None

    @classmethod
    def getVesselByID(cls, vessel_id: int):
        vessel = cls.query.filter_by(id=vessel_id).first()
        if vessel:
            return vessel
        return None
from apis.models.model import db
from apis.models.vessel import Vessel
from flask import jsonify

class Equipment(db.Model):
    __tablename__ = 'equipments'

    id = db.Column(db.BigInteger, primary_key=True)
    vessel_id = db.Column(db.BigInteger, db.ForeignKey('vessels.id'))
    name = db.Column(db.String(256))
    code = db.Column(db.String(8), unique=True)
    location = db.Column(db.String(256))
    active = db.Column(db.Boolean)

    vessels = db.relationship("Vessel", lazy='joined',
                              backref=db.backref('owner', lazy='dynamic'))

    def __init__(self, data: dict, vessel_id: str):
        self.vessel_id = vessel_id,
        self.name = str(data['name']),
        self.code = str(data['code']),
        self.location = str(data['location']),
        self.active = True

    def saveEquipment(self):
        try:
            db.session.add(self)
            db.session.commit()
            return jsonify(
                id=self.id,
                vessel_id=self.vessel_id,
                name=self.name,
                code=self.code,
                location=self.location,
                active=self.active
            )
        except:
            return jsonify(message='Error while trying to save equipment')

    def setInactiveEquipment(self):
        self.active = False

    @classmethod
    def getEquipmentByCode(cls, code: str):
        equipment = cls.query.filter_by(code=code).first()
        if equipment:
            return equipment
        return None

    @classmethod
    def getAllActiveEquipments(cls, vessel_code: str):        
        activeEquipments = [eq for eq in cls.query.filter_by(
            active=True)
            .join(Vessel)
            .filter_by(code=vessel_code)
            .all()]

        return activeEquipments

    @classmethod
    def getAllEquipmentsByName(cls, name: str):
        activeEquipments =[]
        for e, v in db.session.query(Equipment,Vessel).join(Vessel, Equipment.vessel_id == Vessel.id).filter(Equipment.name == name).all():
            activeEquipments.append({"id":e.id, "name": e.name, "code": e.code, "location": e.location, "active": e.active, "vessel_code":v.code})
        return activeEquipments

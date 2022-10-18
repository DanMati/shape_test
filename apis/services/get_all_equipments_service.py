from apis.models.equipment import Equipment
from apis.models.vessel import Vessel
import json

class NullOrEmptyAtribute(ValueError):
    pass

class VesselCodeNotExists(ValueError):
    pass

def obj_dict(obj):
    return obj.__dict__

def get_all_active_equipments_by_vessel(vessel_code):
    
        if len(vessel_code.strip()) == 0:
            raise NullOrEmptyAtribute()

        vessel = Vessel.getVesselByCode(vessel_code)

        if vessel is None:
            raise VesselCodeNotExists()

        equipments = Equipment.getAllActiveEquipments(vessel.code)
        
        equipmentsDict = []

        for equip in equipments:
            equipObj = {
                "id": equip.id,
                "vessel_id": equip.vessel_id,
                "name": equip.name,
                "code": equip.code,
                "location": equip.location,
                "active": equip.active
            }
            equipmentsDict.append(equipObj)

        return equipmentsDict

def get_all_equipments_by_name(name):
    
        if len(name.strip()) == 0:
            raise NullOrEmptyAtribute()
        equipments = Equipment.getAllEquipmentsByName(name)

        equipmentsDict = []

        for equip in equipments:
            equipObj = {
                "id": equip['id'],
                "name": equip['name'],
                "code": equip['code'],
                "location": equip['location'],
                "active": equip['active'],
                "vessel_code":equip['vessel_code']
            }
            equipmentsDict.append(equipObj)

        return equipmentsDict

from apis.models.equipment import Equipment
from apis.models.vessel import Vessel

class NullOrEmptyEquipmentAtribute(ValueError):
    pass

class VesselCodeInvalid(ValueError):
    pass

class EquipmentCodeAlreadyExists(ValueError):
    pass

class EquipmentCodeInvalidSize(ValueError):
    pass

def register_equipment(equipment_request):

    for value in equipment_request.values():
        if(len(value.strip()) == 0):
            raise NullOrEmptyEquipmentAtribute()
    
    if Vessel.getVesselByCode(str(equipment_request['vessel_code'])) == None:
        raise VesselCodeInvalid()
    
    if Equipment.getEquipmentByCode(equipment_request['code']):
        raise EquipmentCodeAlreadyExists()
    
    if len(equipment_request['code']) > 8:
        raise EquipmentCodeInvalidSize()
        
    vessel = Vessel.getVesselByCode(equipment_request['vessel_code'])
    
    equipment = Equipment(equipment_request, vessel.id)
    equipment.saveEquipment()

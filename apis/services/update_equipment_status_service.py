from apis.models.equipment import Equipment

class NullEquipmentCode(ValueError):
    pass

def update_equipment(update_request):
     for equipment in update_request:
            equipmentUpdate = Equipment.getEquipmentByCode(equipment)

            if equipmentUpdate is None:
               raise NullEquipmentCode()

            equipmentUpdate.setInactiveEquipment()
            equipmentUpdate.saveEquipment()

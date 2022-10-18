from apis.models.vessel import Vessel

class NullOrEmptyVesselCode(ValueError):
    pass

class VesselCodeAlreadyExists(ValueError):
    pass
class VesselCodeInvalidSize(ValueError):
    pass

def register_vessel(vessel_code):
    vessel = Vessel(vessel_code)

    if(len(vessel_code.strip()) == 0):
        raise NullOrEmptyVesselCode()

    if(len(vessel_code.strip()) > 8):
        raise VesselCodeInvalidSize()

    if vessel.getVesselByCode(vessel_code):
        raise VesselCodeAlreadyExists()

    vessel.saveVessel()
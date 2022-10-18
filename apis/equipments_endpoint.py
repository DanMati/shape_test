from flask import Blueprint, request, jsonify
from apis.services.register_equipment_service import register_equipment, NullOrEmptyEquipmentAtribute, VesselCodeInvalid, EquipmentCodeAlreadyExists,EquipmentCodeInvalidSize
from apis.services.update_equipment_status_service import update_equipment, NullEquipmentCode
from apis.services.get_all_equipments_service import get_all_active_equipments_by_vessel, get_all_equipments_by_name, NullOrEmptyAtribute,VesselCodeNotExists

equipments_blueprint = Blueprint('equipments', __name__)


@equipments_blueprint.route('/insert_equipment', methods=['POST'])
def insert_equipment():
    """Insert a new equipment
        ---
        parameters:
            - name: vessel_code
              in: body
              type: string
              required: true
            - name: code
              in: body
              type: string
              required: true
            - name: name
              in: body
              type: string
              required: true
            - name: location
              in: body
              type: string
              required: true
        responses:
          201:
            description: returns OK if the equipment was correctly inserted
          400:
            description: returns MISSING_PARAMETER if any parameter is not sent
          400:
            description: returns WRONG_FORMAT if any parameter are sent in the wrong format
          409:
            description: returns REPEATED_CODE if the equipment code is already in the system
          409:
            description: returns NO_VESSEL if the vessel code is not already in the system
    """
    try:
        data = dict(request.json)
        register_equipment(data)
        return jsonify(message="OK"), 201
        
    except KeyError:
        return jsonify(message="MISSING_PARAMETER"), 400
    except NullOrEmptyEquipmentAtribute:
        return jsonify(message="WRONG_FORMAT"), 400
    except VesselCodeInvalid:
        return jsonify(message="NO_VESSEL"), 409
    except EquipmentCodeAlreadyExists:
        return jsonify(message="REPEATED_CODE"), 409
    except EquipmentCodeInvalidSize:
        return jsonify(message="WRONG_FORMAT"), 400


@equipments_blueprint.route('/update_equipment_status', methods=['PUT'])
def update_equipment_status():
    """Set a equipment or a list of those to inactive
        ---
        parameters:
            - name: code
              in: body
              type: string
              required: true
        responses:
          201:
            description: returns OK if the equipments were correctly updated
          400:
            description: returns MISSING_PARAMETER if any parameter is not sent
          400:
            description: returns WRONG_FORMAT if any parameter are sent in the wrong format
          409:
            description: returns NO_CODE if the equipment code is not already in the system
    """
    try:
        data = dict(request.json)
        equipmentsCodes= str(data['code']).split(",")
        update_equipment(equipmentsCodes)
        return jsonify(message="OK"), 201
        
    except KeyError:
        return jsonify(message="MISSING_PARAMETER"), 400
    except NullEquipmentCode:
        return jsonify(message="NO_CODE"), 409
    

@equipments_blueprint.route('/active_equipments', methods=['GET'])
def active_equipment():
    """Return the list of active equipments of a vessel
        ---
        parameters:
            - name: vessel_code
              in: query
              type: string
              required: true
        responses:
          200:
            description: returns a json with equipments key and a list of equipments
          400:
            description: returns MISSING_PARAMETER if the vessel_code is not sent
          400:
            description: returns WRONG_FORMAT if any parameter are sent in the wrong format
          409:
            description: returns NO_VESSEL if the vessel is not already in the system
    """
    try:
      data = request.args['vessel_code']

      equipmentList = get_all_active_equipments_by_vessel(data)
      return jsonify(equipmentList), 200
        
    except KeyError:
        return jsonify(message="MISSING_PARAMETER"), 400
    except NullOrEmptyAtribute:
        return jsonify(message="WRONG_FORMAT"), 400
    except VesselCodeNotExists:
        return jsonify(message="NO_VESSEL"), 409


@equipments_blueprint.route('/equipments_by_name', methods=['GET'])
def get_equipment_by_name():
    """Return the list of active equipments of a vessel by name and which vessel contains it
        ---
        parameters:
            - name: equipment_name
              in: query
              type: string
              required: true
        responses:
          200:
            description: returns a json with equipments key and a list of equipments
          400:
            description: returns MISSING_PARAMETER if the vessel_code is not sent
          400:
            description: returns WRONG_FORMAT if any parameter are sent in the wrong format
          409:
            description: returns NO_VESSEL if the vessel is not already in the system
    """
    try:
      data = request.args['equipment_name']

      equipmentList = get_all_equipments_by_name(data)
      return jsonify(equipmentList), 201
        
    except KeyError:
        return jsonify(message="MISSING_PARAMETER"), 400
    except NullOrEmptyAtribute:
        return jsonify(message="WRONG_FORMAT"), 400
    except VesselCodeInvalid:
        return jsonify(message="NO_VESSEL"), 409

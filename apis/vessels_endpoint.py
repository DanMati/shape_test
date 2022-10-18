from flask import Blueprint, request, jsonify

from apis.models.model import db
from apis.services.register_vessel_service import register_vessel, NullOrEmptyVesselCode, VesselCodeAlreadyExists, VesselCodeInvalidSize

vessels_blueprint = Blueprint('vessels', __name__)


@vessels_blueprint.route('/insert_vessel', methods=['POST'])
def insert_vessel():

    """Insert a new vessel
        ---
        parameters:
            - name: code
              in: body
              type: string
              required: true
        responses:
          201:
            description: returns OK if the vessel was correctly inserted
          400:
            description: returns MISSING_PARAMETER if the vessel code is not sent
          400:
            description: returns WRONG_FORMAT if any parameter are sent in the wrong format
          409:
            description: returns FAIL if the vessel code is already in the system
          422:
            description: returns FAIL if the vessel code is null or empty
    """
    try:
        data = dict(request.json)

        vessel_code = data['code']

        register_vessel(vessel_code)

        return jsonify(message="OK"), 201
    except KeyError:
        return jsonify(message="MISSING_PARAMETER"), 400
    except NullOrEmptyVesselCode:
        return jsonify(message="FAIL"), 422
    except VesselCodeAlreadyExists:
        return jsonify(message="FAIL"), 409
    except VesselCodeInvalidSize:
        return jsonify(message="WRONG_FORMAT"), 400

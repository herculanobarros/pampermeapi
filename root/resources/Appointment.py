from flask import request, json, Response, Blueprint, g
from root.models.Appointment import Appointment, AppointmentSchema
from root.security.Authentication import Auth

appointment_api = Blueprint('appointmens', __name__)
appointment_schema = AppointmentSchema()


# CREATE_APPOINTMENT
@appointment_api.route('/', methods=['POST'])
@Auth.auth_user_required
@Auth.auth_babysitter_required
def create():
    req_data = request.get_json()
    req_data['user_id'] = g.user.get('userId')
    req_data['babysitter_id'] = g.user.get('babysitterId')
    data, error = appointment_schema.load(req_data)
    if error:
        return custom_response(error, 400)
    appointment = Appointment(data)
    appointment.save()
    data = appointment_schema.dump(appointment).data
    return custom_response(data, 201)


def custom_response(res, status_code):
    return Response(
        mimetype="application/json",
        response=json.dumps(res),
        status=status_code
    )

from flask import request
from flask_restful import Resource

from managers.auth import auth
from managers.complaint import ComplaintManager
from models.enums import RoleType
from schemas.request.complaint import ComplaintCreateRequestSchema
from schemas.response.complaint import ComplaintCreateResponseSchema
from utils.decorators import validate_schema, permission_required


class ListCreateComplaint(Resource):
    @auth.login_required
    def get(self):
        complaints = ComplaintManager.get_all()
        schema = ComplaintCreateResponseSchema()
        return schema.dump(complaints, many=True)

    @auth.login_required
    @permission_required(RoleType.complainer)
    @validate_schema(ComplaintCreateRequestSchema)
    def post(self):
        current_user = auth.current_user()
        complaint = ComplaintManager.create(request.get_json(), current_user)
        schema = ComplaintCreateResponseSchema()
        return schema.dump(complaint), 201


class ComplaintDetail(Resource):
    def get(self, id_):
        pass

    @auth.login_required
    @permission_required(RoleType.complainer)
    @validate_schema(ComplaintCreateRequestSchema)
    def put(self, id_):
        update_complaint = ComplaintManager.update(request.get_json(), id_)
        schema = ComplaintCreateResponseSchema()
        return schema.dump(update_complaint)

    @auth.login_required
    # @permission_required(RoleType.admin)
    def delete(self, id_):
        ComplaintManager.delete(id_)
        return {'message': 'Success'}, 204


class ApproveComplaint(Resource):
    @auth.login_required
    # @permission_required(RoleType.approver)
    def put(self, id_):
        complaint = ComplaintManager.approve(id_)
        schema = ComplaintCreateResponseSchema()
        return schema.dump(complaint)


class RejectComplaint(Resource):
    @auth.login_required
    # @permission_required(RoleType.approver)
    def put(self, id_):
        complaint = ComplaintManager.reject(id_)
        schema = ComplaintCreateResponseSchema()
        return schema.dump(complaint)
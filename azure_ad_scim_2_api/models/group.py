from marshmallow import fields, Schema, validate

from azure_ad_scim_2_api.models import BaseResource, DEFAULT_PATCH_OP_SCHEMA, ListResponse

DEFAULT_GROUP_SCHEMA = "urn:ietf:params:scim:schemas:core:2.0:Group"


class GroupMember(Schema):
    value = fields.Str()


class OperationValue(Schema):
    members = fields.List(fields.Nested(GroupMember))


class Operation(Schema):
    op = fields.Str(validate=validate.OneOf(["add", "remove"]))
    value = fields.Nested(OperationValue)
    path = fields.Str()


class PatchGroupOp(Schema):
    schemas = fields.List(fields.Str, default=[DEFAULT_PATCH_OP_SCHEMA])
    operations = fields.List(fields.Nested(Operation), attribute="Operations")


class Group(BaseResource):
    schemas = fields.List(fields.Str, default=[DEFAULT_GROUP_SCHEMA])
    display_name = fields.Str(attribute="displayName")
    members = fields.List(fields.Nested(GroupMember))


class ListGroupsResponse(ListResponse):
    resources = fields.List(
        fields.Nested(Group),
        attribute="Resources",
        default=[]
    )
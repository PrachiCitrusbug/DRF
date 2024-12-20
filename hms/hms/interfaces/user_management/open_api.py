from drf_spectacular.utils import extend_schema_view, OpenApiParameter, extend_schema, OpenApiExample

from .serializers import UserCreateViewSerializer, UserListViewSerializer
from lib.django.custom_models import RoleType

user_view_schema = extend_schema_view(
    list=extend_schema( 
        summary='retrieve-user-list',
        description='This endpoint retrieves all users - only is_staff users are allowed',
        tags=["user"]
    ),
    retrieve=extend_schema(
        summary='retrieve-user-by-id',
        description='This endpoint retrieves a single user information based on id',
        responses=UserListViewSerializer,
        tags=["user"]
    ),
    create=extend_schema(
        summary='create-user',
        description='This endpoint creates a user using payload',
        request=UserCreateViewSerializer,
        responses=UserCreateViewSerializer,
        tags=["user"]
    ),
    update=extend_schema(
        summary='update-user',
        description='This endpoint updates a user using payload',
        request={
                    "application/json": {
                        "type": "object",
                        "properties": {
                            "username": {"type": "string"},
                            "email": {"type": "string"},
                            "role": {
                                "type": "string",
                                "description":
                                    ("**Enum:**\n"
                                    "- `patient`: Patient\n"
                                    "- `doctor`: Doctor\n"
                                    "- `staff`: Staff\n"
                                    "- `superuser`: Superuser"),
                                "enum": [role.value for role in RoleType]
                            },
                        },
                    }
                },
        responses=UserCreateViewSerializer,
        tags=["user"]
    ),
    partial_update=extend_schema(
        summary="partial-update-user",
        description='This endpoint updates a user without asking for all values',
        request={
                    "application/json": {
                        "type": "object",
                        "properties": {
                            "username": {"type": "string"},
                            "email": {"type": "string"},
                            "role": {
                                "type": "string",
                                "description":
                                    ("**Enum:**\n"
                                    "- `patient`: Patient\n"
                                    "- `doctor`: Doctor\n"
                                    "- `staff`: Staff\n"
                                    "- `superuser`: Superuser"),
                                "enum": [role.value for role in RoleType]
                            },
                        },
                    }
                },
        responses=UserCreateViewSerializer,
        tags=["user"]
    ),
    destroy=extend_schema(
        summary="delete-user",
        description="This endpoint deletes the requested user",
        tags=["user"]
    )
)

# parameters=[OpenApiParameter(
        #     name="search",
           
        #     required=False,
        #     type=str,
        #     enum = 
        # )],
# examples=[OpenApiExample(
            #     name="search",
            #     value={
            #         "search": "username|email"
            #     }
            # )],

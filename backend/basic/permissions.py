from rest_framework import permissions, status, exceptions
from .models import EventRoleMapping, Registration
from rest_framework.response import Response


def get_eventrole(request, view, event_role_id):
    return EventRoleMapping.objects.filter(event_id=view.kwargs.get("event_pk", None),
                                           user=request.user, event_role_id__in=event_role_id).exists()


class IsEventMaster(permissions.BasePermission):
    message = 'Nur für die Fahrtenleitung.'

    def has_permission(self, request, view):
        return get_eventrole(request, view, [1, ])


class IsEventCashMaster(permissions.BasePermission):
    message = 'Nur für das Kassenteam oder Fahrtenleitung.'

    def has_permission(self, request, view):
        return get_eventrole(request, view, [1, 2])


class IsKitchenMaster(permissions.BasePermission):
    message = 'Nur für das Kücheteam oder Fahrtenleitung.'

    def has_permission(self, request, view):
        return get_eventrole(request, view, [1, 3])


class IsProgramMaster(permissions.BasePermission):
    message = 'Nur für das Programmtean oder Fahrtenleitung.'

    def has_permission(self, request, view):
        return get_eventrole(request, view, [1, 4])


class IsLogisticMaster(permissions.BasePermission):
    message = 'Nur für das Logistikteam oder Fahrtenleitung.'

    def has_permission(self, request, view):
        return get_eventrole(request, view, [1, 5])


class IsSocialMediaPermission(permissions.BasePermission):
    message = 'Nur für das Öffentlichkeitsteam oder Fahrtenleitung.'

    def has_permission(self, request, view):
        return get_eventrole(request, view, [1, 6])


class IsTeamMemberPermission(permissions.BasePermission):
    message = 'Nur für das Planungsteam'

    def has_permission(self, request, view):
        return get_eventrole(request, view, [1, 2, 3, 4, 5, 6])


class IsResponsiblePersonPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        pk = view.kwargs.get("registration_pk") or view.kwargs.get("pk") or view.kwargs.get("pk") or \
             ('registration' in request.data and request.data['registration'])
        if pk is None:
            raise NoRegistationId()
        return Registration.objects.filter(id=pk, responsible_persons=request.user).exists()


class NoRegistationId(exceptions.APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "No Registration id given"

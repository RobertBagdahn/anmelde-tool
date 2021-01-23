from rest_framework import permissions
from .models import EventRoleMapping, Registration


def get_eventrole(request, view, event_role_id):
    return EventRoleMapping.objects.filter(event_id=view.kwargs.get("event_pk", None),
                                           user=request.user, event_role_id__in=event_role_id).exists()


class IsEventMaster(permissions.BasePermission):
    message = 'Nur für die Lagerleitung.'

    def has_permission(self, request, view):
        return get_eventrole(request, view, [1, ])


class IsEventCashMaster(permissions.BasePermission):
    message = 'Nur für das Kassenteam oder Lagerleitung.'

    def has_permission(self, request, view):
        return get_eventrole(request, view, [1, 2])


class IsKitchenMaster(permissions.BasePermission):
    message = 'Nur für das Kücheteam oder Lagerleitung.'

    def has_permission(self, request, view):
        return get_eventrole(request, view, [1, 3])


class IsProgramMaster(permissions.BasePermission):
    message = 'Nur für das Programmtean oder Lagerleitung.'

    def has_permission(self, request, view):
        return get_eventrole(request, view, [1, 4])


class IsLogisticMaster(permissions.BasePermission):
    message = 'Nur für das Logistikteam oder Lagerleitung.'

    def has_permission(self, request, view):
        return get_eventrole(request, view, [1, 5])


class IsSocialMediaPermission(permissions.BasePermission):
    message = 'Nur für das Öffentlichkeitsteam oder Lagerleitung.'

    def has_permission(self, request, view):
        return get_eventrole(request, view, [1, 6])


class IsResponsiblePersonPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        pk = view.kwargs.get("registration_pk") or request.data['registration']
        return Registration.objects.filter(id=pk, responsible_persons=request.user).exists()

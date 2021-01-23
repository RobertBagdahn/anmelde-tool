# views.py
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets, mixins
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from helper.user_creation import CreateUserExternally
from rest_framework.response import Response
from .models import Event, AgeGroup, EventLocation, ScoutHierarchy, Registration, \
    ZipCode, ParticipantGroup, ParticipantRole, Role, MethodOfTravel, Tent, \
    ScoutOrgaLevel, ParticipantPersonal, EatHabitType, EatHabit, TravelType, \
    TentType, EatHabit

from .serializers import EventSerializer, AgeGroupSerializer, EventLocationSerializer, \
    ScoutHierarchySerializer, RegistrationSerializer, ZipCodeSerializer, ParticipantGroupSerializer, \
    ParticipantRoleSerializer, RoleSerializer, MethodOfTravelSerializer, TentSerializer, \
    EventParticipantsSerializer, ScoutOrgaLevelSerializer, ParticipantPersonalSerializer, \
    EatHabitTypeSerializer, EatHabitSerializer, TravelTypeSerializer, \
    TentTypeSerializer, EventOverviewSerializer, EatHabitSerializer, EventCashMasterSerializer, \
    EventKitchenMasterSerializer, EventProgramMasterSerializer, RegistrationParticipantsSerializer

from .permissions import IsEventMaster, IsKitchenMaster, IsEventCashMaster, IsProgramMaster, \
    IsLogisticMaster, IsSocialMediaPermission, IsResponsiblePersonPermission


def get_dataset(kwargs, pk, dataset):
    dataset_id = kwargs.get(pk, None)
    print(dataset_id)
    if dataset_id is not None:
        return dataset.objects.filter(id=dataset_id)
    else:
        return Response('No dataset selected', status=status.HTTP_400_BAD_REQUEST)


def get_event(kwargs):
    event_id = kwargs.get("event_pk", None)
    if event_id is not None:
        return Event.objects.filter(id=event_id)
    else:
        return Response('No event selected', status=status.HTTP_400_BAD_REQUEST)


class EventViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Event.objects.all()
    serializer_class = EventSerializer


class EventOverviewViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Event.objects.all()
    serializer_class = EventOverviewSerializer


class AgeGroupViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = AgeGroup.objects.all()
    serializer_class = AgeGroupSerializer


class EventLocationViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = EventLocation.objects.all()
    serializer_class = EventLocationSerializer


class ScoutHierarchyViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = ScoutHierarchy.objects.all().exclude(level=6)
    serializer_class = ScoutHierarchySerializer


class ScoutHierachyGroupViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ScoutHierarchySerializer

    def get_queryset(self):
        return ScoutHierarchy.objects.filter(level=6, parent=self.request.user.userextended.scout_organisation)


class RegistrationViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Registration.objects.all()
    serializer_class = RegistrationSerializer

    def create(self, request, *args, **kwargs):
        # Check responsible person
        emails = request.data['responsible_persons']
        for user_email in emails:
            user = User.objects.filter(username=user_email).first()
            if user is None:
                CreateUserExternally(user_email)
                # TODO: Add mail for notifiction as registered as responsible person

        # Check invitation code
        queryset = Event.objects.all()
        event = get_object_or_404(queryset, pk=request.data['event'])

        if 'code' in self.request.query_params:
            code = self.request.query_params.get('code', None)
        else:
            return Response({'code': 'missing query param'}, status=status.HTTP_400_BAD_REQUEST)

        if event.invitation_code != code:
            raise PermissionDenied('wrong invitation code')

        return super().create(request, *args, **kwargs)


class ZipCodeViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = ZipCode.objects.all()
    serializer_class = ZipCodeSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['zip_code']


class ParticipantGroupViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = ParticipantGroup.objects.all()
    serializer_class = ParticipantGroupSerializer


class ParticipantRoleViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = ParticipantRole.objects.all()
    serializer_class = ParticipantRoleSerializer


class RoleViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Role.objects.all()
    serializer_class = RoleSerializer


class MethodOfTravelViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = MethodOfTravel.objects.all()
    serializer_class = MethodOfTravelSerializer


class TentViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Tent.objects.all()
    serializer_class = TentSerializer


class ScoutOrgaLevelViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = ScoutOrgaLevel.objects.all()
    serializer_class = ScoutOrgaLevelSerializer


class ParticipantPersonalViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsResponsiblePersonPermission]
    queryset = ParticipantPersonal.objects.all()
    serializer_class = ParticipantPersonalSerializer

    def create(self, request, *args, **kwargs):
        # Check whether habit type exists
        if 'eat_habit_type' in request.data:
            habit_types = request.data['eat_habit_type']
            for type in habit_types:
                if not EatHabitType.objects.filter(name__exact=type).exists():
                    new_type = EatHabitType.objects.create(name=type)
                    new_type.save()

        # Check whether group name exits
        if 'scout_group' in request.data:
            scout_group = request.data['scout_group']
            if not ScoutHierarchy.objects.filter(name__exact=scout_group, level__id=6).exists():
                new_group = ScoutHierarchy.objects.create(name=scout_group, level=ScoutOrgaLevel.objects.get(pk=6),
                                                          parent=request.user.userextended.scout_organisation)
                new_group.save()
                print('created new group: ', new_group)

        return super().create(request, *args, **kwargs)


class EatHabitTypeViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = EatHabitType.objects.all()
    serializer_class = EatHabitTypeSerializer


class EatHabitViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = EatHabit.objects.all()
    serializer_class = EatHabitSerializer

    def create(self, request, *args, **kwargs):
        # Check whether habit type exists
        if 'eat_habit_type' in request.data:
            print(request.data['eat_habit_type'])
            habit_types = request.data['eat_habit_type']
            for type in habit_types:
                print(type)
                if not EatHabitType.objects.filter(name__exact=type).exists():
                    new_type = EatHabitType.objects.create(name=type)
                    new_type.save()

        return super().create(request, *args, **kwargs)


class TravelTypeViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = TravelType.objects.all()
    serializer_class = TravelTypeSerializer


class TentTypeViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = TentType.objects.all()
    serializer_class = TentTypeSerializer


class EventCodeCheckerViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, pk=None):
        queryset = Event.objects.all()
        event = get_object_or_404(queryset, pk=pk)

        if 'code' in self.request.query_params:
            code = self.request.query_params.get('code', None)
        else:
            return Response({'code': 'missing query param'}, status=status.HTTP_400_BAD_REQUEST)

        if event.invitation_code == code:
            return Response({'status': 'Code correct'}, status=status.HTTP_200_OK)
        else:
            raise PermissionDenied('wrong invitation code')


class EventMasterViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated, IsEventMaster]
    serializer_class = EventCashMasterSerializer

    def get_queryset(self):
        return get_event(self.kwargs)


class EventCashMasterViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated, IsEventCashMaster]
    serializer_class = EventCashMasterSerializer

    def get_queryset(self):
        return get_event(self.kwargs)


class EventKitchenMasterViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated, IsKitchenMaster]
    serializer_class = EventKitchenMasterSerializer

    def get_queryset(self):
        return get_event(self.kwargs)


class EventProgramMasterViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated, IsProgramMaster]
    serializer_class = EventProgramMasterSerializer

    def get_queryset(self):
        return get_event(self.kwargs)


class EventParticipantsViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = EventParticipantsSerializer

    def get_queryset(self):
        return get_event(self.kwargs)


class RegistrationParticipantsViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated, IsResponsiblePersonPermission]
    serializer_class = RegistrationParticipantsSerializer

    def get_queryset(self):
        event_id = self.kwargs.get("registration_pk", None)
        if event_id is not None:
            return Registration.objects.filter(id=event_id)
        else:
            return Response('No registration selected', status=status.HTTP_400_BAD_REQUEST)

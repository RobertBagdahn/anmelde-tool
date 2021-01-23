# serializers.py
from rest_framework import serializers
from .models import Event, AgeGroup, EventLocation, ScoutHierarchy, Registration, ZipCode, \
    ParticipantGroup, ParticipantRole, Role, MethodOfTravel, Tent, ScoutOrgaLevel, ParticipantPersonal, \
    EatHabitType, EatHabit, TravelType, TentType
from rest_framework.fields import Field
from django.contrib.auth.models import User
from django.db.models import Sum, Count, F, Q, Func, Subquery, Value, When, Case
from django.db.models.functions import Coalesce
from django.db.models.functions import Length, Upper


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'


class EventOverviewSerializer(serializers.ModelSerializer):
    participant_role = serializers.SerializerMethodField('get_event_role')
    is_registered = serializers.SerializerMethodField('get_is_registered')

    class Meta:
        model = Event
        fields = (
            'id',
            'name',
            'description',
            'event_tags',
            'start_time',
            'end_time',
            'participant_role',
            'is_registered',
        )

    def get_event_role(self, obj):
        roles = obj.eventrolemapping_set.filter(user=self.context['request'].user).values_list('event_role_id',
                                                                                               flat=True)
        if roles:
            return roles
        else:
            return []

    def get_is_registered(self, obj):
        res = obj.registration_set.filter(
            scout_organisation=self.context['request'].user.userextended.scout_organisation).values('is_confirmed',
                                                                                                    'is_accepted')
        if res:
            return res
        else:
            return False


class AgeGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = AgeGroup
        fields = '__all__'


class EventLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventLocation
        fields = '__all__'


class ScoutHierarchySerializer(serializers.ModelSerializer):
    class Meta:
        model = ScoutHierarchy
        fields = '__all__'


class RegistrationSerializer(serializers.ModelSerializer):
    responsible_persons = serializers.SlugRelatedField(
        many=True,
        read_only=False,
        queryset=User.objects.all(),
        slug_field='username'
    )

    class Meta:
        model = Registration
        fields = '__all__'


class ZipCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ZipCode
        fields = '__all__'


class ParticipantGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParticipantGroup
        fields = '__all__'


class EventParticipantsSerializer(serializers.ModelSerializer):
    locations = serializers.SerializerMethodField('get_locations')

    class Meta:
        model = Event
        fields = (
            'locations',
        )

    def get_bund_name(self, scout_organisation):
        if scout_organisation.level_id > 3:
            return self.get_bund_name(scout_organisation.parent)
        elif scout_organisation.level_id < 3:
            raise Exception("To low value")
        else:
            return scout_organisation.name

    def get_locations(self, obj):

        result = obj.registration_set.values('scout_organisation__name').annotate(
            participants=Coalesce(Sum('participantgroup__number_of_persons'), 0) +
                         Coalesce(Count('participantpersonal'), 0),
            bund=Case(When(scout_organisation__level=3,
                           then=F('scout_organisation__name')),
                      When(scout_organisation__parent__level=3,
                           then=F('scout_organisation__parent__name')),
                      When(scout_organisation__parent__parent__level=3,
                           then=F('scout_organisation__parent__parent__name')))) \
            .values('scout_organisation__name',
                    'participants',
                    'bund',
                    lon=Coalesce(F('scout_organisation__zip_code__lon'), 0),
                    lat=Coalesce(F('scout_organisation__zip_code__lat'), 0),
                    )

        return result


class RegistrationParticipantsSerializer(serializers.ModelSerializer):
    participants = serializers.SerializerMethodField('get_participants')

    class Meta:
        model = Registration
        fields = (
            'event',
            'participants'
        )

    def get_participants(self, obj):
        return obj.participantpersonal_set.values()


class ParticipantRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParticipantRole
        fields = '__all__'


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'


class MethodOfTravelSerializer(serializers.ModelSerializer):
    class Meta:
        model = MethodOfTravel
        fields = '__all__'


class TentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tent
        fields = '__all__'


class ScoutOrgaLevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScoutOrgaLevel
        fields = '__all__'


class ParticipantPersonalSerializer(serializers.ModelSerializer):
    eat_habit_type = serializers.SlugRelatedField(
        many=True,
        read_only=False,
        queryset=EatHabitType.objects.all(),
        slug_field='name'
    )

    scout_group = serializers.SlugRelatedField(
        many=False,
        read_only=False,
        queryset=ScoutHierarchy.objects.filter(level=6),
        slug_field='name'
    )

    class Meta:
        model = ParticipantPersonal
        fields = '__all__'


class EatHabitTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = EatHabitType
        fields = '__all__'


class EatHabitSerializer(serializers.ModelSerializer):
    eat_habit_type = serializers.SlugRelatedField(
        many=True,
        read_only=False,
        queryset=EatHabitType.objects.all(),
        slug_field='name'
    )

    class Meta:
        model = EatHabit
        fields = '__all__'


class TravelTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TravelType
        fields = '__all__'


class TentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TentType
        fields = '__all__'


class EventCashMasterSerializer(serializers.ModelSerializer):
    total_participants = serializers.SerializerMethodField('get_total_participants')
    total_fee = serializers.SerializerMethodField('get_total_fee')
    grouped_participants = serializers.SerializerMethodField('get_grouped_participants')

    class Meta:
        model = Event
        fields = ('total_participants',
                  'participation_fee',
                  'total_fee',
                  'grouped_participants',
                  )

    def get_total_participants(self, obj):
        self.participants = obj.registration_set.aggregate(
            total_participants=Sum('participantgroup__number_of_persons') + Count('participantpersonal'))[
            'total_participants']
        return self.participants

    def get_total_fee(self, obj):
        return obj.participation_fee * self.participants

    def get_grouped_participants(self, obj):
        return obj.registration_set.values('scout_organisation', 'scout_organisation__name') \
            .annotate(grouped_participants=Coalesce(Sum('participantgroup__number_of_persons'), 0),
                      single_participants=Coalesce(Count('participantpersonal'), 0)) \
            .values('scout_organisation__name',
                    'grouped_participants',
                    'single_participants',
                    total_amount=F('grouped_participants') + F('single_participants'),
                    total_fee=F('total_amount') * obj.participation_fee)


class EventKitchenMasterSerializer(serializers.ModelSerializer):
    total_participants = serializers.SerializerMethodField('get_total_participants')
    num_vegetarien = serializers.SerializerMethodField('get_num_vegetarien')
    num_vegan = serializers.SerializerMethodField('get_num_vegan')
    num_grouped_by_age_group = serializers.SerializerMethodField('get_num_grouped_by_age_group')
    num_grouped_by_age_personal = serializers.SerializerMethodField('get_num_grouped_by_age_personal')

    class Meta:
        model = Event
        fields = ('total_participants',
                  'num_vegetarien',
                  'num_vegan',
                  'num_grouped_by_age_group',
                  'num_grouped_by_age_personal')

    def get_total_participants(self, obj):
        return obj.registration_set.aggregate(
            total_participants=Sum('participantgroup__number_of_persons') + Count('participantpersonal'))[
            'total_participants']

    def get_num_vegetarien(self, obj):
        return obj.registration_set.aggregate(veggi_group=Sum('participantgroup__eathabit__number_of_persons',
                                                              filter=Q(participantgroup__eathabit__eat_habit_type=1)),
                                              veggi_personal=Count('participantpersonal',
                                                                   filter=Q(participantpersonal__eat_habit_type=1)),
                                              veggie_total=F('veggi_group') + F('veggi_personal'))

    def get_num_vegan(self, obj):
        return obj.registration_set.aggregate(vegan_group=Sum('participantgroup__eathabit__number_of_persons',
                                                              filter=Q(participantgroup__eathabit__eat_habit_type=2)),
                                              vegan_personal=Count('participantpersonal',
                                                                   filter=Q(participantpersonal__eat_habit_type=2)),
                                              vegan_total=F('vegan_group') + F('vegan_personal'))

    def get_num_grouped_by_age_group(self, obj):
        result = obj.registration_set.values(age_group_group=F('participantgroup__age_group__name'),
                                             habit_type_group=F('participantgroup__eathabit__eat_habit_type__name')) \
            .annotate(number_group=Coalesce(Sum('participantgroup__eathabit__number_of_persons'), 0)) \
            .order_by('-participantgroup__age_group')
        return result

    def get_num_grouped_by_age_personal(self, obj):
        # TODO: Improve result by combaining different habits
        result = obj.registration_set.values(age_group_personal=F('participantpersonal__age_group__name'),
                                             habit_type_personal=F('participantpersonal__eat_habit_type__name')) \
            .annotate(number_personal=Coalesce(Count('participantpersonal__eat_habit_type'), 0)) \
            .order_by('-participantpersonal__age_group')
        return result


class EventProgramMasterSerializer(serializers.ModelSerializer):
    total_participants = serializers.SerializerMethodField('get_total_participants')
    participants_grouped_by_age = serializers.SerializerMethodField('get_participants_grouped_by_age')

    class Meta:
        model = Event
        fields = ('total_participants',
                  'participants_grouped_by_age',
                  )

    def get_total_participants(self, obj):
        return obj.registration_set.aggregate(
            total_participants=Sum('participantgroup__number_of_persons') + Count('participantpersonal'))[
            'total_participants']

    def get_participants_grouped_by_age(self, obj):
        return obj.registration_set.values(
            age_group_group=F('participantgroup__age_group__name'),
            age_group_personal=F('participantpersonal__age_group__name')) \
            .annotate(number_group=Coalesce(Sum('participantgroup__number_of_persons'), 0),
                      number_personal=Coalesce(Count('participantpersonal'), 0))

# serializers.py
from django.contrib.postgres.aggregates import ArrayAgg
from rest_framework import serializers
from .models import Event, AgeGroup, EventLocation, ScoutHierarchy, Registration, ZipCode, \
    ParticipantGroup, Role, MethodOfTravel, Tent, ScoutOrgaLevel, ParticipantPersonal, \
    EatHabitType, EatHabit, TravelType, TentType, TravelTag, PostalAddress
from rest_framework.fields import Field
from django.contrib.auth.models import User
from django.db.models import Sum, Count, F, Q, Func, Subquery, Case, When
from django.db.models.functions import Coalesce
from itertools import combinations


def distinct_combinations(num_range):
    result = []
    for r in num_range:
        comb = list(combinations(num_range, r))
        result.append(comb)
    return [item for sublist in result for item in sublist]


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
            'registration_start',
            'registration_deadline',
            'end_time',
            'participant_role',
            'is_registered'
        )

    def get_event_role(self, obj):
        roles = obj.eventrolemapping_set.filter(user=self.context['request'].user).values(
            'event_role_id',
            'event_role__name')

        if roles:
            return roles
        else:
            return []

    def get_is_registered(self, obj):
        return obj.registration_set.filter(
            scout_organisation=self.context['request'].user.userextended.scout_organisation).values(
            'id',
            'is_confirmed',
            'is_accepted'
        )


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
    scout_organisations = serializers.SerializerMethodField('get_scout_organisations')
    registration_date = serializers.SerializerMethodField('get_registration_date')

    class Meta:
        model = Event
        fields = (
            'scout_organisations',
            'registration_date'
        )

    def get_scout_organisations(self, obj):
        result = obj.registration_set.values('scout_organisation__name').annotate(
            participants=Coalesce(Sum('participantgroup__number_of_persons'), 0)
                         + Coalesce(Count('participantpersonal'), 0),
            bund=Case(When(scout_organisation__parent__parent__parent__level=3,
                           then=F('scout_organisation__parent__parent__parent__name')),
                      When(scout_organisation__parent__parent__level=3,
                           then=F('scout_organisation__parent__parent__name')),
                      When(scout_organisation__parent__level=3,
                           then=F('scout_organisation__parent__name')),
                      When(scout_organisation__level=3,
                           then=F('scout_organisation__name')))
        ).values('scout_organisation__name',
                 'participants',
                 'bund',
                 lon=F('scout_organisation__zip_code__lon'),
                 lat=F('scout_organisation__zip_code__lat'),
                 )

        return result

    def get_registration_date(self, obj):
        result = obj.registration_set.values('scout_organisation__name', 'participantgroup__created_at__date',
                                             'participantpersonal__created_at__date').annotate(
            participants=Coalesce(Sum('participantgroup__number_of_persons'), 0)
                         + Coalesce(Count('participantpersonal'), 0),
            bund=Case(When(scout_organisation__parent__parent__parent__level=3,
                           then=F('scout_organisation__parent__parent__parent__name')),
                      When(scout_organisation__parent__parent__level=3,
                           then=F('scout_organisation__parent__parent__name')),
                      When(scout_organisation__parent__level=3,
                           then=F('scout_organisation__parent__name')),
                      When(scout_organisation__level=3,
                           then=F('scout_organisation__name')))
        ).values('scout_organisation__name',
                 'participants',
                 'bund',
                 created_at=Case(When(participantgroup__created_at__date__isnull=False,
                                      then=F('participantgroup__created_at__date')),
                                 When(participantpersonal__created_at__date__isnull=False,
                                      then=F('participantpersonal__created_at__date'))),

                 lon=F('scout_organisation__zip_code__lon'),
                 lat=F('scout_organisation__zip_code__lat'),
                 )

        return result


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


class TravelTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = TravelTag
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
            total_participants=Coalesce(Sum('participantgroup__number_of_persons'), 0) + Count('participantpersonal'))[
            'total_participants']
        return self.participants

    def get_total_fee(self, obj):
        if self.participants:
            return obj.participation_fee * self.participants

        return 0

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
    num_without_anything = serializers.SerializerMethodField('get_num_without_anything')
    num_vegetarien = serializers.SerializerMethodField('get_num_vegetarien')
    num_vegan = serializers.SerializerMethodField('get_num_vegan')
    num_grouped_by_age_group = serializers.SerializerMethodField('get_num_grouped_by_age_group')
    num_grouped_by_age_personal = serializers.SerializerMethodField('get_num_grouped_by_age_personal')
    food_grouped = serializers.SerializerMethodField('get_food_grouped')

    class Meta:
        model = Event
        fields = ('total_participants',
                  'num_without_anything',
                  'num_vegetarien',
                  'num_vegan',
                  'num_grouped_by_age_group',
                  'num_grouped_by_age_personal',
                  'food_grouped'
                  )

    def get_total_participants(self, obj):
        return obj.registration_set.aggregate(
            total_participants=Coalesce(Sum('participantgroup__number_of_persons'), 0) + Count('participantpersonal'))[
            'total_participants']

    def get_num_without_anything(self, obj):
        res_group = obj.registration_set.filter(participantgroup__eathabit__isnull=True).count()
        res_pers = obj.registration_set.filter(participantpersonal__eat_habit_type__isnull=True).count()
        return res_group + res_pers

    def get_num_vegetarien(self, obj):
        return obj.registration_set.aggregate(veggi_group=Coalesce(Sum('participantgroup__eathabit__number_of_persons',
                                                                       filter=
                                                                       Q(participantgroup__eathabit__eat_habit_type=1)),
                                                                   0)
                                                          + Count('participantpersonal',
                                                                  filter=Q(participantpersonal__eat_habit_type=1)))[
            'veggi_group']

    def get_num_vegan(self, obj):
        return obj.registration_set.aggregate(vegan_total=Coalesce(Sum('participantgroup__eathabit__number_of_persons',
                                                                       filter=
                                                                       Q(participantgroup__eathabit__eat_habit_type=2)),
                                                                   0)
                                                          + Count('participantpersonal',
                                                                  filter=Q(participantpersonal__eat_habit_type=2)))[
            'vegan_total']

    def get_num_grouped_by_age_group(self, obj):
        result = obj.registration_set.values(age_group_group=F('participantgroup__age_group__name'),
                                             habit_type_group=F('participantgroup__eathabit__eat_habit_type__name')) \
            .annotate(number_group=Coalesce(Sum('participantgroup__eathabit__number_of_persons'), 0)) \
            .exclude(age_group_group__isnull=True).exclude(habit_type_group__isnull=True) \
            .order_by('-participantgroup__age_group')
        return result

    def get_num_grouped_by_age_personal(self, obj):
        # TODO: Improve result by combaining different habits
        result = obj.registration_set.values(age_group_personal=F('participantpersonal__age_group__name'),
                                             habit_type_personal=F('participantpersonal__eat_habit_type__name')) \
            .annotate(number_personal=Coalesce(Count('participantpersonal__eat_habit_type'), 0)) \
            .exclude(age_group_personal__isnull=True).exclude(habit_type_personal__isnull=True) \
            .order_by('-participantpersonal__age_group')
        return result

    def get_food_grouped(self, obj):
        habit_types = list(EatHabitType.objects.values_list('id', flat=True))
        all_combination = distinct_combinations(habit_types)

        result = []
        list_id = []

        ids = list(obj.registration_set.values_list('id', flat=True))
        total_participants = ParticipantPersonal.objects.filter(registration__in=ids)

        for combination in all_combination:
            comb_opposite = list([elem for elem in habit_types if elem not in combination])
            num_pariticpants = total_participants.filter(eat_habit_type=combination) \
                .exclude(eat_habit_type__in=comb_opposite).exclude(id__in=list_id).values_list('id', flat=True)

            list_id.extend(num_pariticpants)
            num_result = num_pariticpants.count()

            json = {
                'eat_habit_type': EatHabitType.objects.filter(id__in=combination).values_list('name', flat=True),
                'num_participants': num_result
            }

            result.append(json)
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
        return obj.registration_set.values(role=Case(
            When(participantgroup__participant_role__isnull=False, then=F('participantgroup__participant_role__name')),
            When(participantpersonal__participant_role__isnull=False,
                 then=F('participantpersonal__participant_role__name')))
        ).aggregate(total_participants=Coalesce(Sum('participantgroup__number_of_persons'), 0)
                                       + Count('participantpersonal'))['total_participants']

    def get_participants_grouped_by_age(self, obj):
        return obj.registration_set.values(role=Case(
            When(participantgroup__participant_role__isnull=False, then=F('participantgroup__participant_role__name')),
            When(participantpersonal__participant_role__isnull=False,
                 then=F('participantpersonal__participant_role__name'))),
            age_group=Case(When(participantgroup__age_group__isnull=False,
                                then=F('participantgroup__age_group__name')),
                           When(participantpersonal__age_group__isnull=False,
                                then=F('participantpersonal__age_group__name')))) \
            .annotate(number_group=Coalesce(Sum('participantgroup__number_of_persons'), 0),
                      number_personal=Coalesce(Count('participantpersonal'), 0)) \
            .exclude(role__isnull=True).exclude(age_group__isnull=True)

        return result


class RegistrationSummarySerializer(serializers.ModelSerializer):
    total_participants = serializers.SerializerMethodField('get_total_participants')
    total_fee = serializers.SerializerMethodField('get_total_fee')
    group_participants = serializers.SerializerMethodField('get_group_participants')
    personal_participants = serializers.SerializerMethodField('get_personal_participants')
    travel_method = serializers.SerializerMethodField('get_travel_method')
    travel_method_detailed = serializers.SerializerMethodField('get_travel_method_detailed')
    tents = serializers.SerializerMethodField('get_tents')
    tents_detailed = serializers.SerializerMethodField('get_tents_detailed')
    responsible_persons = serializers.SerializerMethodField('get_responsible_persons')
    locations = serializers.SerializerMethodField('get_locations')
    postaladdress = serializers.SerializerMethodField('get_postaladdress')


    scout_organisation = serializers.SlugRelatedField(
        many=False,
        read_only=False,
        queryset=ScoutHierarchy.objects.all(),
        slug_field='name'
    )

    event = serializers.SlugRelatedField(
        many=False,
        read_only=False,
        queryset=Event.objects.all(),
        slug_field='name'
    )

    class Meta:
        model = Registration
        fields = (
            'scout_organisation',
            'event',
            'responsible_persons',
            'free_text',
            'total_participants',
            'total_fee',
            'group_participants',
            'personal_participants',
            'is_confirmed',
            'is_accepted',
            'travel_method',
            'travel_method_detailed',
            'tents',
            'tents_detailed',
            'postaladdress',
            'locations',
            'custom_choice'
        )

    def get_locations(self, obj):
        result = obj.eventlocation_set.values("name",
                                              "address",
                                              "description",
                                              "description",
                                              "contact_name",
                                              "contact_email",
                                              "contact_phone",
                                              "capacity",
                                              "per_person_fee",
                                              "fix_fee",
                                              "capacity_corona",
                                              "zip_code__zip_code",
                                              "location_type__name",
                                              "location_type__id",
                                              )

        return result

    def get_postaladdress(self, obj):
        result = obj.postaladdress_set.values("first_name",
                                              "last_name",
                                              "street",
                                              "address_addition",
                                              "zip_code__zip_code",
                                              )

        return result

    def get_responsible_persons(self, obj):
        result = obj.responsible_persons.values('username',
                                                "userextended__scout_name",
                                                "userextended__mobile_number")
        return result

    def get_total_participants(self, obj):
        num_group = obj.participantgroup_set.aggregate(num=Coalesce(Sum('number_of_persons'), 0))['num']
        num_pers = obj.participantpersonal_set.count()
        result = num_group + num_pers
        self.total_participants = result
        return result

    def get_total_fee(self, obj):
        return obj.event.participation_fee * self.total_participants

    def get_group_participants(self, obj):
        result = obj.participantgroup_set.values('participant_role_id').annotate(
            registered=Coalesce(Sum('number_of_persons'), 0)).values(
                "participant_role_id__name", "participant_role_id", "registered"
            )

        return result

    def get_personal_participants(self, obj):
        result = obj.participantpersonal_set.values('created_at__date').annotate(registered=Count('id')) \
            .order_by('-created_at__date')
        return result

    def get_travel_method(self, obj):
        return obj.methodoftravel_set.values('travel_type__name').annotate(
            sum_method=Coalesce(('number_of_persons'), 0))

    def get_travel_method_detailed(self, obj):
        return obj.methodoftravel_set.values('travel_type__name').values('travel_type__name', 'number_of_persons')

    def get_tents(self, obj):
        return obj.tent_set.values('tent_type__name').annotate(sum_tents=Count('tent_type'))

    def get_tents_detailed(self, obj):
        return obj.tent_set.values('tent_type__name', 'used_by_scout_groups__name')


class RegistrationParticipantsSerializer(serializers.ModelSerializer):
    participantpersonal_set = ParticipantPersonalSerializer(read_only=True, many=True)

    class Meta:
        model = Registration
        fields = (
            'event',
            'participantpersonal_set'
        )


class PostalAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostalAddress
        fields = '__all__'

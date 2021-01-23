import base64

from django.db import models
from django.contrib.auth.models import User
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP


class TimeStampMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        abstract = True


class ZipCode(TimeStampMixin):
    id = models.AutoField(
        auto_created=True,
        primary_key=True,
        serialize=False,
        verbose_name='ID')
    zip_code = models.CharField(max_length=5, blank=True)
    city = models.CharField(max_length=60, blank=True)
    lat = models.DecimalField(max_digits=20, decimal_places=15, default=0.000)
    lon = models.DecimalField(max_digits=20, decimal_places=15, default=0.000)

    def __str__(self):
        return self.zip_code + ' - ' + self.city

    def __repr__(self):
        return self.__str__()


class EventLocationType(TimeStampMixin):
    id = models.AutoField(
        auto_created=True,
        primary_key=True,
        serialize=False,
        verbose_name='ID')
    name = models.CharField(max_length=20)
    description = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.__str__()


class EventLocation(TimeStampMixin):
    id = models.AutoField(
        auto_created=True,
        primary_key=True,
        serialize=False,
        verbose_name='ID')
    name = models.CharField(max_length=60)
    description = models.CharField(max_length=200, blank=True)
    location_type = models.ForeignKey(EventLocationType, on_delete=models.PROTECT, null=True, blank=True)
    zip_code = models.ForeignKey(ZipCode, on_delete=models.PROTECT, null=True, blank=True)
    address = models.CharField(max_length=60, blank=True)
    contact_name = models.CharField(max_length=30, blank=True)
    contact_email = models.CharField(max_length=30, blank=True)
    contact_phone = models.CharField(max_length=30, blank=True)
    is_public = models.BooleanField(default=0)
    capacity_indoor = models.IntegerField(blank=True, null=True)
    capacity_outdoor = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.__str__()


class AgeGroup(TimeStampMixin):
    id = models.AutoField(
        auto_created=True,
        primary_key=True,
        serialize=False,
        verbose_name='ID')
    name = models.CharField(max_length=20)
    description = models.CharField(max_length=100, blank=True)
    min_age = models.IntegerField(blank=True, null=True)
    max_age = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.__str__()


class Role(TimeStampMixin):
    id = models.AutoField(
        auto_created=True,
        primary_key=True,
        serialize=False,
        verbose_name='ID')
    name = models.CharField(max_length=20)
    description = models.CharField(max_length=100, blank=True)
    force_email = models.BooleanField(default=0)

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.__str__()


class ScoutOrgaLevel(TimeStampMixin):
    id = models.AutoField(
        auto_created=True,
        primary_key=True,
        serialize=False,
        verbose_name='ID')
    name = models.CharField(max_length=20)
    description = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.__str__()


class ScoutHierarchy(TimeStampMixin):
    id = models.AutoField(
        auto_created=True,
        primary_key=True,
        serialize=False,
        verbose_name='ID')
    level = models.ForeignKey(ScoutOrgaLevel, on_delete=models.PROTECT, null=True, blank=True)
    name = models.CharField(max_length=60, blank=True)
    zip_code = models.ForeignKey(ZipCode, on_delete=models.PROTECT, null=True, blank=True)
    parent = models.ForeignKey('self', null=True, on_delete=models.PROTECT, related_name='scouthierarchy', blank=True)

    def __str__(self):
        return "{} - {}".format(self.level, self.name)

    def __repr__(self):
        return self.__str__()


class EventTag(TimeStampMixin):
    id = models.AutoField(
        auto_created=True,
        primary_key=True,
        serialize=False,
        verbose_name='ID')
    name = models.CharField(max_length=20)
    description = models.CharField(max_length=100, blank=True)


class Event(TimeStampMixin):
    id = models.AutoField(
        auto_created=True,
        primary_key=True,
        serialize=False,
        verbose_name='ID')
    name = models.CharField(max_length=20)
    description = models.CharField(max_length=100, blank=True)
    location = models.ForeignKey(EventLocation, on_delete=models.PROTECT, null=True, blank=True)
    age_groups = models.ManyToManyField(AgeGroup, blank=True)
    event_tags = models.ManyToManyField(EventTag, blank=True)
    start_time = models.DateTimeField(auto_now=False, auto_now_add=False, null=True, blank=True)
    end_time = models.DateTimeField(auto_now=False, auto_now_add=False, null=True, blank=True)
    registration_deadline = models.DateTimeField(auto_now=False, auto_now_add=False, null=True, blank=True)
    registration_start = models.DateTimeField(auto_now=False, auto_now_add=False, null=True, blank=True)
    participation_fee = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    min_helper = models.IntegerField(blank=True, null=True)
    min_participation = models.IntegerField(blank=True, null=True)
    max_participation = models.IntegerField(blank=True, null=True)
    invitation_code = models.CharField(max_length=6, blank=True)
    max_scout_orga_level = models.ForeignKey(ScoutOrgaLevel, on_delete=models.PROTECT, null=True, blank=True)
    is_public = models.BooleanField(default=0)
    public_key = models.CharField(max_length=1000, blank=True)

    # ToDo: add pdf attatchment
    # ToDo: add html description

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.__str__()


class EventRole(TimeStampMixin):
    id = models.AutoField(
        auto_created=True,
        primary_key=True,
        serialize=False,
        verbose_name='ID')
    name = models.CharField(max_length=20)
    description = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.__str__()


class EventRoleMapping(TimeStampMixin):
    id = models.AutoField(
        auto_created=True,
        primary_key=True,
        serialize=False,
        verbose_name='ID')
    event = models.ForeignKey(Event, on_delete=models.PROTECT)
    event_role = models.ForeignKey(EventRole, on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.PROTECT)


class Registration(TimeStampMixin):
    id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    scout_organisation = models.ForeignKey(ScoutHierarchy, on_delete=models.PROTECT, null=True, blank=True)
    responsible_persons = models.ManyToManyField(User)
    event = models.ForeignKey(Event, on_delete=models.PROTECT, null=True, blank=True)
    free_text = models.CharField(max_length=1000, blank=True)
    is_confirmed = models.BooleanField(default=0)
    is_accepted = models.BooleanField(default=0)


class ParticipantGroup(TimeStampMixin):
    id = models.AutoField(
        auto_created=True,
        primary_key=True,
        serialize=False,
        verbose_name='ID')
    number_of_persons = models.IntegerField(blank=True, null=True)
    age_group = models.ForeignKey(AgeGroup, on_delete=models.PROTECT, null=True, blank=True)
    registration = models.ForeignKey(Registration, on_delete=models.PROTECT, null=True, blank=True)


class EatHabitType(TimeStampMixin):
    id = models.AutoField(
        auto_created=True,
        primary_key=True,
        serialize=False,
        verbose_name='ID')
    name = models.CharField(max_length=40)
    description = models.CharField(max_length=100, blank=True)
    is_custom = models.BooleanField(default=1)

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.__str__()


class ParticipantPersonal(TimeStampMixin):
    id = models.AutoField(
        auto_created=True,
        primary_key=True,
        serialize=False,
        verbose_name='ID')
    registration = models.ForeignKey(Registration, on_delete=models.PROTECT, null=True, blank=True)
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    street = models.CharField(max_length=100, blank=True)
    zip_code = models.ForeignKey(ZipCode, on_delete=models.PROTECT, null=True, blank=True)
    date_birth = models.DateField(auto_now=False, auto_now_add=False, null=True, blank=True)
    scout_group = models.ForeignKey(ScoutHierarchy, on_delete=models.PROTECT, null=True, blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    is_group_leader = models.BooleanField(default=0)
    age_group = models.ForeignKey(AgeGroup, on_delete=models.PROTECT, null=True, blank=True)
    eat_habit_type = models.ManyToManyField(EatHabitType, blank=True)

    def save(self, *args, **kwargs):
        if not self.pk:
            print(self)
            # pub_key = self.registration.event.public_key

            pub_key = '-----BEGIN RSA PUBLIC KEY-----\nMIIBCgKCAQEAnGyAwxcp8qwRYvnvGQvDnj/HzeIg+gDh3TIbgUmJaAPo+9+pP1FwzqytpstF\ngO1lKG+Ja8k3ryP9L1fN6KMDVTZK22OnezKreRUsRYwuBTaHZF3mnBrcZCfEn++E69IRL4CQ\n159crAfJAG8F87RjqPkTZxtXDmedQAbTjFrApKo9FPyWTCSw+beYuKihvHgVrlto8oeXhgoT\nbSNGLFKW7FvSAy29J6mqVVvH/hvCCXCqIOwf+I3YHs691KOrofS+kWZCxmM9K7SyxgDZprup\nJdQSIp3Iv0JFUIKfmoHBd19V5ZvMv0kj5mNuj7n0jbbbmVmtpawqoeQfk2AufCg9UwIDAQAB\n-----END RSA PUBLIC KEY-----'
            priv_key = '-----BEGIN RSA PRIVATE KEY-----\nMIIEpQIBAAKCAQEAnGyAwxcp8qwRYvnvGQvDnj/HzeIg+gDh3TIbgUmJaAPo+9+pP1Fwzqyt\npstFgO1lKG+Ja8k3ryP9L1fN6KMDVTZK22OnezKreRUsRYwuBTaHZF3mnBrcZCfEn++E69IR\nL4CQ159crAfJAG8F87RjqPkTZxtXDmedQAbTjFrApKo9FPyWTCSw+beYuKihvHgVrlto8oeX\nhgoTbSNGLFKW7FvSAy29J6mqVVvH/hvCCXCqIOwf+I3YHs691KOrofS+kWZCxmM9K7SyxgDZ\nprupJdQSIp3Iv0JFUIKfmoHBd19V5ZvMv0kj5mNuj7n0jbbbmVmtpawqoeQfk2AufCg9UwID\nAQABAoIBAFs4n4KmII1nsSACV2BIzwSbd17mj4qcNxuy2/1ysBIbraQtU9scGGg+pWpOwrKk\nPsjs+rwD9VhK6ZzRXMBdSFVKOy9kF0iuTPdo1I+eZzwdB6oNZK4GsB4sXutSWDbaI7GLDWzh\nf77HL330QQlVWoUw9BK+C+/Xlwm+sWH5jry3rU0k5033hsrGse6C9nekAVSNJplxka9xL5CS\nv8Wrbx3nN5GgK+o9PtzclYqSYW3l5vVrM/CQm3a71GvC4COMHJreelMZHj/S5n1L6AgTu8KM\naInGDcyFxJnarcmYnUnp8ZNBkS15UFWYki3wdxQqAv82pdVuf36wPMlEM309DaECgYEAybWj\nT0F58EAHA8da6GWyMwmKoWh9MH0M5FJFbLJRpKLz72pbH/irIZSRx+J3u667kEChooSfdGMl\nGJi/7wxWlQJcLmhKGnZxcbMPmUEOXXCd54AFbnShXqNjg1LN9HD9EfTNANoSpAdTLgUGbmSo\nwNlz8zxQRf1yeS0O4GupEnECgYEAxoaNWnKEg6KocE78YyzrUm1PiujTh5amotGShoeL0NVe\ntku9uaseRsZTVOuHHX6wKloGEKzNYx1SL30DvBzcO+DpUTJ2gABjn+t0IFHFds1sskKGZ38g\nIiArKbpyevzxyQiIMbHmrYip3UU+LycZPhn1I/f0nsPcSGSpyJsUZgMCgYEAyZPB7rSKfbQe\nzoHtsY3f9e01I3TelxSBS7OEOcpCmPtYOAzboCnMK7TjsxP5gBBw1Qoh/d331EI4kkoklWqJ\nJETFhoMmeyee23eMwSUoi+y9gNqJkwbvNTqnelfIBt7bqZQxQwar1kyTrcvLz4q8sm0d2RiP\nSEKuobaLxW8R+aECgYEAqOZeqn3VidzAK1S323Si/KytSMRO+wNL4Cgm3jfB1zlA7B1CXA1e\no94llZEQkiJvpIiUsmkiEFooyug0Xj27jWILfp5NPReXqr36PWj0c9/Pw1Vf3fvFDeOKdWT/\n8uzylBOjM4xkcm1b/zni7uD30+LnseNKBi0iY6Do5hgyYZsCgYEAjplzym1oWAi2NMft+7MS\nqEcjsO1kvux3+ZEQ4CWYAknfpqisn1kfUuAxto/pR6aJTxYZXfR0eXa3xBRVYa/3zfeiZ+QH\ns9Ivug9yUKdHo7qqYjNGP3VUoWa+G+p9rzwBtK9ineb5aDKZqqWZhgpGh6DxAC78PcORQBDW\n2KgVnYQ=\n-----END RSA PRIVATE KEY-----'

            keyPub = RSA.importKey(pub_key)
            keyPriv = RSA.importKey(priv_key)
            encryptor = PKCS1_OAEP.new(keyPub)

            encrypted = encryptor.encrypt(self.first_name.encode(('utf-8')))
            self.first_name = base64.b64encode(encrypted)

            decryptor = PKCS1_OAEP.new(keyPriv)
            decrypted = decryptor.decrypt(encrypted)

            print(decrypted)
            super(ParticipantPersonal, self).save(*args, **kwargs)


class ParticipantRole(TimeStampMixin):
    id = models.AutoField(
        auto_created=True,
        primary_key=True,
        serialize=False,
        verbose_name='ID')
    participant_personal = models.ForeignKey(ParticipantPersonal, on_delete=models.PROTECT, null=True, blank=True)
    event = models.ForeignKey(Event, on_delete=models.PROTECT, null=True, blank=True)
    role = models.ForeignKey(Role, on_delete=models.PROTECT, null=True, blank=True)


class EatHabit(models.Model):
    id = models.AutoField(
        auto_created=True,
        primary_key=True,
        serialize=False,
        verbose_name='ID')
    eat_habit_type = models.ForeignKey(EatHabitType, on_delete=models.PROTECT, null=True, blank=True)
    participant_group = models.ForeignKey(ParticipantGroup, on_delete=models.PROTECT, null=True, blank=True)
    number_of_persons = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.__str__()


class TravelType(TimeStampMixin):
    id = models.AutoField(
        auto_created=True,
        primary_key=True,
        serialize=False,
        verbose_name='ID')
    name = models.CharField(max_length=20)
    description = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.__str__()


class MethodOfTravel(TimeStampMixin):
    id = models.AutoField(
        auto_created=True,
        primary_key=True,
        serialize=False,
        verbose_name='ID')
    registration = models.ForeignKey(Registration, on_delete=models.PROTECT, null=True, blank=True)
    travel_type = models.ForeignKey(TravelType, on_delete=models.PROTECT, null=True, blank=True)
    number_of_persons = models.IntegerField(blank=True, null=True)


class TentType(TimeStampMixin):
    id = models.AutoField(
        auto_created=True,
        primary_key=True,
        serialize=False,
        verbose_name='ID')
    name = models.CharField(max_length=20)
    description = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.__str__()


class Tent(TimeStampMixin):
    id = models.AutoField(
        auto_created=True,
        primary_key=True,
        serialize=False,
        verbose_name='ID')
    registration = models.ForeignKey(Registration, on_delete=models.PROTECT, null=True, blank=True)
    tent_type = models.ForeignKey(TentType, on_delete=models.PROTECT, null=True, blank=True)
    used_by_scout_groups = models.ManyToManyField(ScoutHierarchy, blank=True)

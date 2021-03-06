<template>
  <v-container class="top-margin">
    <v-row justify="center">
      <v-flex ma-3 lg9>
        <v-layout column>
          <v-card v-if="!isLoading">
            <v-card-title class="text-center justify-center py-6">
              Zu diesen Fahrten kannst du deinen Stamm anmelden
            </v-card-title>
            <v-list subheader two-line>
              <v-subheader inset>
                Nicht lange zögern. Melde deinen Stamm zu einer dieser
                Fahrten an.
              </v-subheader>

              <v-btn
                class="ma-6"
                color="success"
                v-if="isAuthenticated && !isSimpleUser"
                @click="$router.push({ name: 'createEvent' })"
              >
                <v-icon left>mdi-calendar-plus</v-icon>
                Neue Fahrt erstellen
              </v-btn>
                <v-divider/>
              <template v-for="(item, index) in getItems">
                <v-list-item :key="item.name">
                  <v-list-item-avatar>
                    <v-icon
                      :class="'primary'"
                      dark
                      v-text="'mdi-tent'"
                    ></v-icon>
                  </v-list-item-avatar>
                  <v-list-item-content>
                    <v-list-item-title
                      v-text="getHeaderText(item.name, item.participantRole)"
                    ></v-list-item-title>

                    <v-list-item-subtitle
                      v-text="item.description"
                    ></v-list-item-subtitle>

                    <v-list-item-subtitle>
                      {{ getLagerText(item) }}
                    </v-list-item-subtitle>

                    <v-list-item-subtitle>
                      {{ getDeadline(item) }}
                    </v-list-item-subtitle>
                  </v-list-item-content>

                  <v-list-item-action
                    v-show="
                      isInTimeRange(
                        item.registrationStart,
                        item.registrationDeadline,
                      ) && !item.isRegistered.length
                    "
                  >
                    <router-link
                      :to="{
                        name: 'registrationForm',
                        params: {
                          id: item.id,
                        },
                      }"
                      style="text-decoration: none"
                    >
                      <v-tooltip bottom>
                        <template v-slot:activator="{ on, attrs }">
                          <v-btn icon v-bind="attrs" v-on="on">
                            <v-icon fab color="primary">
                              mdi-account-multiple-plus
                            </v-icon>
                          </v-btn>
                        </template>
                        <span>Fahrtenanmeldung</span>
                      </v-tooltip>
                    </router-link>
                  </v-list-item-action>

                  <v-list-item-action
                    v-show="
                      isInTimeRange(
                        item.registrationStart,
                        item.registrationDeadline,
                      ) && item.isRegistered.length
                    "
                    class="ml-4"
                  >
                    <v-btn icon
                           v-if="item.isRegistered.length"
                           @click="editRegistration(getRegisteredId(item))">
                      <v-icon fab color="primary"> mdi-pencil </v-icon>
                    </v-btn>
                  </v-list-item-action>

                  <v-list-item-action>
                    <router-link
                      :to="{
                        name: 'statisticOverview',
                        params: { id: item.id },
                      }"
                      style="text-decoration: none"
                      v-if="item.participantRole.length"
                    >
                      <v-tooltip bottom>
                        <template v-slot:activator="{ on, attrs }">
                          <v-btn icon v-bind="attrs" v-on="on">
                            <v-icon fab color="primary"> mdi-chart-bar </v-icon>
                          </v-btn>
                        </template>
                        <span>Fahrtenstatistik</span>
                      </v-tooltip>
                    </router-link>
                  </v-list-item-action>
                </v-list-item>
                <v-divider
                  v-if="index < getItems.length - 1"
                  :key="index"
                ></v-divider>
              </template>
            </v-list>
          </v-card>
          <v-card v-else>
            <div class="text-center ma-5">
              <p> Lade Daten ...</p>
              <v-progress-circular
                :size="80"
                :width="10"
                class="ma-5"
                color="primary"
                indeterminate
              ></v-progress-circular>
              <p> Bitte hab etwas Geduld.</p>
            </div>
          </v-card>
        </v-layout>
      </v-flex>
    </v-row>
    <confirm-registration-edit-modal ref="confirmRegistrationEditModal"/>
  </v-container>
</template>

<script>
import axios from 'axios';
import moment from 'moment';
import { mapGetters } from 'vuex';
// eslint-disable-next-line import/extensions
import ConfirmRegistrationEditModal from '@/views/registration/create/steps/dialog/ConfirmRegistrationEditModal';

export default {
  components: { ConfirmRegistrationEditModal },
  data: () => ({
    components: {
      ConfirmRegistrationEditModal,
    },
    API_URL: process.env.VUE_APP_API,
    items: [],
    isLoading: true,
    userExtendedItems: [],
    headers: [
      { text: 'Id', value: 'id' },
      { text: 'Fahrt', value: 'name' },
      { text: 'Beschreibung', value: 'description' },
      { text: 'Actions', value: 'action', sortable: false },
    ],
  }),

  computed: {
    ...mapGetters(['isAuthenticated', 'getJwtData']),
    getItems() {
      return this.items;
    },
    hasSetExtendedUserInfos() {
      if (this.userExtendedItems) {
        return (
          this.userExtendedItems.scoutName && // eslint-disable-line
          this.userExtendedItems.scoutOrganisation
        );
      }
      return false;
    },
    isSimpleUser() {
      if (this.getJwtData) {
        return !(this.getJwtData.groups.length || this.getJwtData.isStaff);
      }
      return true;
    },
  },
  methods: {
    editRegistration(item) {
      this.$refs.confirmRegistrationEditModal.show(item);
    },
    getHeaderText(header, roles) {
      if (roles && roles.length) {
        return `${header} (Deine Rolle: ${roles[0].eventRole_Name})`;
      }
      return header;
    },
    getRegisteredId(item) {
      if (
        item && // eslint-disable-line
        item.isRegistered && // eslint-disable-line
        item.isRegistered.length && // eslint-disable-line
        item.isRegistered[0].id
      ) {
        return item.isRegistered[0].id;
      }
      return 0;
    },
    isInTimeRange(date1, date2) {
      const startTime = new Date(date1).getTime();
      const endTime = new Date(date2).getTime();
      const today = new Date().getTime();

      return today > startTime && today < endTime;
    },
    getLagerText(item) {
      const startTime = new Date(item.startTime);
      const endTime = new Date(item.endTime);
      const dateFormat = 'll';

      const text1 = `Termin: ${moment(startTime)
        .lang('de')
        .format(dateFormat)} bis ${moment(endTime)
        .lang('de')
        .format(dateFormat)}`;
      return text1;
    },
    getDeadline(item) {
      const dateFormat = 'll';
      const registrationDeadline = new Date(item.registrationDeadline);
      const text2 = `Anmeldeschluss: ${moment(registrationDeadline)
        .lang('de')
        .format(dateFormat)}`;
      return text2;
    },
    async getEvent() {
      const path = `${this.API_URL}basic/event-overview/`;
      const response = await axios.get(path);

      return response.data;
    },
    async getUserExtended() {
      const { userId } = this.getJwtData;
      const ts = new Date().getTime();
      const path = `${this.API_URL}auth/data/user-extended/${userId}/?&timestamp=${ts}`;
      const response = await axios.get(path);

      return response.data;
    },
    async getRoleMapping() {
      const path = `${this.API_URL}basic/role/`;
      const response = await axios.get(path);

      return response.data;
    },
    async getScoutOrgaLevelMapping() {
      const path = `${this.API_URL}basic/scout-orga-level/`;
      const response = await axios.get(path);

      return response.data;
    },
    async getEatHabitTypeMapping() {
      const path = `${this.API_URL}basic/eat-habit-type/`;
      const response = await axios.get(path);

      return response.data;
    },

    async getTravelTypeMapping() {
      const path = `${this.API_URL}basic/travel-type/`;
      const response = await axios.get(path);

      return response.data;
    },
    async getHierarchyMapping() {
      const path = `${process.env.VUE_APP_API}basic/scout-hierarchy/`;
      const response = await axios.get(path);

      return response.data;
    },
    async getAgeGroupMapping() {
      const path = `${this.API_URL}basic/age-group/`;
      const response = await axios.get(path);

      return response.data;
    },
    async getTentTypeMapping() {
      const path = `${this.API_URL}basic/tent-type/`;
      const response = await axios.get(path);

      return response.data;
    },
    onGoToSettingsButtonClicked() {
      this.goToSettings();
    },
    goToSettings() {
      this.$router.push({ name: 'settingsUser' });
    },
    show(item) {
      this.$refs.messageModal.show(item);
    },
    onRegistrationClicked() {
      this.$router.push({ name: 'registrationForm' });
    },
  },
  mounted() {
    this.isLoading = true;

    Promise.all([
      this.getEvent(),
      this.getUserExtended(),
      this.getRoleMapping(),
      this.getScoutOrgaLevelMapping(),
      this.getEatHabitTypeMapping(),
      this.getTravelTypeMapping(),
      this.getHierarchyMapping(),
      this.getAgeGroupMapping(),
      this.getTentTypeMapping(),
    ])
      .then((values) => {
        [this.items, this.userExtendedItems] = values;

        this.$store.commit('setRoleMapping', values[2]);
        this.$store.commit('setScoutOrgaLevelMapping', values[3]);
        this.$store.commit('setEatHabitTypeMapping', values[4]);
        this.$store.commit('setTravelTypeTypeMapping', values[5]);
        this.$store.commit('setHierarchyMapping', values[6]);
        this.$store.commit('setAgeGroupMapping', values[7]);
        this.$store.commit('setTentTypeMapping', values[8]);

        if (!this.hasSetExtendedUserInfos) {
          this.goToSettings();
        }

        this.isLoading = false;
      })
      .catch((error) => {
        this.errormsg = error.response.data.message;
        this.isLoading = false;
      });
  },
};
</script>

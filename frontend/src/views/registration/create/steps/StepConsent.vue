<template>
  <v-form ref="formNameDescription" v-model="valid">
    <v-container v-if="!isLoading">
      <v-row class="mt-2">
        <span class="text-left subtitle-1">
          <p>
            Hiermit melde ich <b> {{ myStamm }} </b> zur
            <b> {{ currentEvent.name }} </b> an. <br />
            <br />
            Bevor deine Anmeldung verbindlich wird, musst du sie im letzten
            Schritt ausdrücklich bestätigen. Du kannst deinen Anmeldevorgang zu
            jedem Zeitpunkt unterbrechen und später fortsetzen. Die Daten kannst du
            bis zum Anmeldeschluss ({{ registrationDeadlineFormat }}) jederzeit
            anpassen und ergänzen. <br />
            <br />
            Die folgenden Daten sind nur für das Planungsteam und die Administrator_innen
            sichtbar. <br />
          </p>
          <p>
            <br />
            Hinweis: Vergiss nicht dich als Fahrtenleitung auch selbst anzumelden.
            <br />
          </p>
        </span>
      </v-row>
      <v-divider class="text-left my-2" />
      <v-row>
        <v-checkbox
          v-model="data.checkbox1"
          :label="`Ich stimme den Bedingungen zu und möchte mit der Anmeldung beginnen.`"
          :error-messages="checkbox1Errors"
        >
        </v-checkbox>
      </v-row>

      <v-row>
        <v-checkbox
          v-model="data.checkbox2"
          v-if="isBundesfahrt"
          :label="`Hiermit bestätige ich, dass alle Teilnehmer_innen,
          die ich auf diesem Wege zur Bundesfahrt anmelde die
          „Datenschutzhinweise zur Bundesfahrt 2021 des DPBM“ zur
          Kenntnis genommen und diesen zugestimmt haben.`"
          :error-messages="checkbox2Errors"
        >
        </v-checkbox>
      </v-row>

      <v-divider class="my-3" />

      <prev-next-buttons
        :position="position"
        :max-pos="maxPos"
        @nextStep="nextStep"
        @prevStep="prevStep"
      />
    </v-container>
    <v-container v-else>
      <div class="text-center ma-5">
        <p>Lade Daten ...</p>
        <v-progress-circular
          :size="80"
          :width="10"
          class="ma-5"
          color="primary"
          indeterminate
        ></v-progress-circular>
        <p>Bitte hab etwas Geduld.</p>
      </div>
    </v-container>
  </v-form>
</template>

<script>
import { mapGetters } from 'vuex';
import moment from 'moment';
import axios from 'axios';

import { required } from 'vuelidate/lib/validators';
import PrevNextButtons from '../components/button/PrevNextButtonsSteps.vue';

export default {
  name: 'StepConsent',
  displayName: 'Einverständnis',
  props: [
    'position',
    'maxPos',
    'currentEvent',
    'currentRegistration',
    'scoutOrganisation',
  ],
  components: {
    PrevNextButtons,
  },
  data: () => ({
    API_URL: process.env.VUE_APP_API,
    valid: true,
    isLoading: true,
    data: {
      checkbox1: false,
      checkbox2: false,
      name: '',
      description: '',
    },
  }),
  validations: {
    data: {
      checkbox1: {
        required,
        checked: (value) => value === true,
      },
      checkbox2: {
        function(value) {
          return value === true || !this.isBundesfahrt;
        },
      },
    },
  },
  computed: {
    ...mapGetters(['isAuthenticated', 'hierarchyMapping', 'getJwtData']),
    checkbox1Errors() {
      const errors = [];
      if (!this.$v.data.checkbox1.$dirty) return errors;
      if (!this.$v.data.checkbox1.required || !this.$v.data.checkbox1.checked) {
        errors.push(
          'Deine Zustimmung ist erforderlich, damit du weiter machen kannst.',
        );
      }
      return errors;
    },
    checkbox2Errors() {
      const errors = [];
      if (!this.$v.data.checkbox2.$dirty) return errors;
      if (this.$v.data.checkbox2.$invalid) {
        errors.push(
          'Deine Zustimmung ist erforderlich, damit du weiter machen kannst.',
        );
      }
      return errors;
    },
    myStamm() {
      if (this.extendedUsers.scoutOrganisation) {
        return this.hierarchyMapping.find(
          (item) => item.id === this.extendedUsers.scoutOrganisation,
        ).name;
      }
      return 'Keine Name';
    },
    registrationDeadlineFormat() {
      return moment(this.currentEvent.registrationDeadline)
        .lang('de')
        .format('ll');
    },
    myEmail() {
      return this.getJwtData.email;
    },
    isBundesfahrt() {
      if (this.currentEvent) {
        return this.currentEvent.eventTags.filter((tag) => tag === 1).length;
      }
      return false;
    },
  },
  mounted() {
    this.beforeTabShow();
  },
  methods: {
    validate() {
      this.$v.$touch();
      this.valid = !this.$v.$error;
    },
    prevStep() {
      this.$emit('prevStep');
    },
    nextStep() {
      this.validate();
      if (!this.valid) {
        return;
      }
      this.$emit('nextStep');
    },
    beforeTabShow() {
      this.loadData();
    },
    loadData() {
      this.isLoading = true;

      Promise.all([this.loadUserExtended()])
        .then((values) => {
          [this.extendedUsers] = values;
          this.isLoading = false;
        })
        .catch((error) => {
          this.errormsg = error.response.data.message;
          this.isLoading = false;
        });
    },
    async loadUserExtended() {
      const path = `${this.API_URL}auth/data/user-extended/${this.getJwtData.userId}/`;
      const response = await axios.get(path);

      return response.data;
    },
  },
};
</script>

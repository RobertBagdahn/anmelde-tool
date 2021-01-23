<template>
  <v-form ref="StepBdpDpVPreferences" v-model="valid">
    <v-container class="px-0" fluid>
      <v-expand-transition>
        <v-container>
          <span>
            Unser Lagerplatz oder Heim hat eine Möglichkeit zum Kochen (Herd/
            Feuerstelle) ausreichend Toiletten (Dixi/ WC) fließend Wasser.
          </span>
          <v-radio-group v-model="radioGroup">
            <v-radio
              label="Wir wollen bei uns in der Stadt bleiben"
              value="1"
            ></v-radio>
            <v-radio
              label="Wir wollen nicht bei uns in der Stadt bleiben."
              value="2"
            ></v-radio>
            <v-radio label="Uns ist beides recht." value="22"></v-radio>
          </v-radio-group>
        </v-container>
      </v-expand-transition>

      <v-expand-transition>
        <v-container v-show="radioGroup === '1'">
          <span>
            Unser Lagerplatz oder Heim hat eine Möglichkeit zum Kochen (Herd/
            Feuerstelle) ausreichend Toiletten (Dixi/ WC) fließend Wasser.
          </span>
          <v-divider class="my-4" />
          <v-radio-group v-model="radioGroup2">
            <v-radio
              v-show="dpvAddedLocation"
              label="Wir wollen einen anderen Stamm zu uns einladen"
              value="3"
            ></v-radio>
            <v-radio
              v-show="dpvAddedLocation"
              label="Wir wollen einen anderen Stamm in unserer Stadt besuchen (und stellen
        unser Heim/ Lagerplatz anderen Stämmen zur Verfügung)"
              value="5"
            ></v-radio>
            <v-radio
              v-show="!dpvAddedLocation"
              label="Wir wollen einen anderen Stamm in unserer Stadt besuchen."
              value="5"
            ></v-radio>
          </v-radio-group>
        </v-container>
      </v-expand-transition>

      <v-expand-transition>
        <v-container v-show="radioGroup === '2'">
          <v-divider class="my-4" />
          <v-radio-group v-model="radioGroup2">
            <v-radio label="Wir fahren gern weit weg. " value="3"></v-radio>
            <v-radio
              label="Wir möchten gern in der Nähe unserer Stadt bleiben. "
              value="5"
            ></v-radio>
          </v-radio-group>
        </v-container>
      </v-expand-transition>

      <v-expand-transition>
        <v-checkbox
          v-show="dpvAddedLocation"
          v-model="data.checkbox1"
          :label="`Wir stellen unser Heim / Lagerplatz anderen Stämmen zur Verfügung.)`"
        />
        <v-divider class="my-3" />
      </v-expand-transition>

      <prev-next-buttons
        :position="position"
        :max-pos="maxPos"
        @nextStep="nextStep()"
        @prevStep="prevStep"
        @submitStep="submitStep()"
      />
    </v-container>
    <create-location-dialog ref="newLocationDialog" @close="getEvents()" />
  </v-form>
</template>

<script>
import { mapGetters } from 'vuex';

import CreateLocationDialog from '@/views/event/create/components/dialog/CreateLocationDialog.vue';
import PrevNextButtons from '../components/button/PrevNextButtonsSteps.vue';

export default {
  name: 'StepBdpDpvLocation',
  displayName: 'Wo soll es hingehen?',
  props: ['position', 'maxPos'],
  components: {
    PrevNextButtons,
    CreateLocationDialog,
  },
  data: () => ({
    API_URL: process.env.VUE_APP_API,
    valid: true,
    radioGroup: 0,
    radioGroup2: 0,
    data: {
      value1: true,
      value2: false,
    },
  }),
  computed: {
    ...mapGetters(['dpvAddedLocation']),
  },
  validations: {},
  methods: {
    newLocation() {
      this.$refs.newLocationDialog.openDialog();
    },
    validate() {
      this.$v.$touch();
      console.log(!this.$v.$error);
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
    submitStep() {
      this.validate();
      if (!this.valid) {
        return;
      }
      this.$emit('submit');
    },
    getData() {
      return {
        name: this.data.name,
        description: this.data.description,
      };
    },
  },
};
</script>

<style>
</style>

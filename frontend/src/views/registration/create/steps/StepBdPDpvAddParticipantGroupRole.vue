<template>
  <v-form ref="formParticipantGroupRole" v-model="valid">
    <v-container>
      <p>
        Du kannst die Anzahl der Teilnehmenden bis zum 1. Mai 2021 anpassen.
        <br />
        <br />
        Dafür kannst du dich jederzeit wieder einloggen. <br />
        <br />
        Diese Anmeldung bezieht sich auf das gesamte Wochenende. Personen, die
        früher fahren oder später kommen zählen als vollwertige teilnehmende
        Person.<br>
        <br>
        Vergiss nicht dich selbst auch mitzuzählen.
        <v-icon class="mx-2" color="red">mdi-account-alert</v-icon>
      </p>
      <v-form v-model="valid">
        <v-divider class="py-3 mt-5" />
        <v-row>
          <v-col col="12">
            <v-slider
              v-model="normal"
              color="orange"
              label="Teilnehmende"
              min="1"
              max="200"
              thumb-label="always"
            >
            </v-slider>
            <v-row class="ml-5">
              <p>
                <v-icon color="success" dark> mdi-help-circle-outline </v-icon>
                {{ tooltip.normal }}
              </p>
            </v-row>
          </v-col>
        </v-row>
        <v-divider class="py-4 ma-0" />
        <v-row>
          <v-col col="12">
            <v-slider
              v-model="groupLeader"
              color="grey"
              label="Gruppenleitung"
              min="0"
              max="30"
              thumb-label="always"
              type="number"
            />
            <v-row class="ml-5">
              <p>
                <v-icon color="success" dark> mdi-help-circle-outline </v-icon>
                {{ tooltip.groupLeader }}
              </p>
            </v-row>
          </v-col>
        </v-row>
        <v-divider class="py-4 ma-0" />
        <v-row>
          <v-col col="12">
            <v-slider
              v-model="stammes"
              color="blue"
              label="Stammesvertretung"
              min="1"
              max="3"
              thumb-label="always"
              type="number"
            />
            <v-row class="ml-5">
              <p>
                <v-icon color="success" dark> mdi-help-circle-outline </v-icon>
                {{ tooltip.stammes }}
              </p>
            </v-row>
          </v-col>
        </v-row>
        <v-divider class="py-4 ma-0" />
        <v-row>
          <v-col col="12">
            <v-slider
              v-model="helper"
              color="red"
              label="Helferlein"
              min="0"
              max="50"
              thumb-label="always"
              type="number"
            />
            <v-row class="ml-5">
              <p>
                <v-icon color="success" dark> mdi-help-circle-outline </v-icon>
                {{ tooltip.helper }}
              </p>
            </v-row>
          </v-col>
        </v-row>
        <v-divider class="py-4 ma-0" />
        <v-row>
          <v-col col="12">
            <v-slider
              v-model="total"
              color="green"
              label="Gesamt"
              thumb-label="always"
              max="200"
              type="number"
              readonly
            >
            </v-slider>
          </v-col>
        </v-row>
      </v-form>
      <v-divider class="py-4 ma-0" />
      {{
        `Du hast ${total} Personen angemeldet. Das entspricht einem Stammesbeitrag von maximal ${
          total * 10
        } €.`
      }}
    </v-container>
    <v-divider class="my-3" />

    <prev-next-buttons
      :position="position"
      :max-pos="maxPos"
      @nextStep="nextStep()"
      @prevStep="prevStep"
      @submitStep="submitStep()"
    />
  </v-form>
</template>

<script>
import axios from 'axios';

import PrevNextButtons from '../components/button/PrevNextButtonsSteps.vue';
// import RolePicker from '../components/RolePicker..vue';

export default {
  name: 'StepAddParticipantGroupRole',
  displayName: 'Teilnehmende',

  components: {
    // RolePicker,
    PrevNextButtons,
  },
  props: ['position', 'maxPos'],
  data: () => ({
    API_URL: process.env.VUE_APP_API,
    tooltip: {
      normal:
        'Das sind die Kinder/Jugendlichen in den Gruppen, die aktiv am Spiel teilnehmen.',
      groupLeader:
        'Auch diese nehmen aktiv am Spiel teil und haben die Aufsichtspflicht.',
      stammes:
        'Hier sind lediglich wenige Menschen pro Stamm notwendig (max. 3, eher weniger), auch sie nehmen aktiv am Spiel teil und haben Koordinationsaufgaben.',
      helper:
        'Alle, die keine Lust haben auf der aktiven Spielseite zu stehen, sondern lieber hinter oder auf der Bühne die Fäden ziehen wollen, können sich hier melden.',
      total: 'Many ist eine Tomate',
    },
    displayName: 'Essgewohnheiten',
    normal: 0,
    helper: 0,
    stammes: 0,
    groupLeader: 0,
    normalId: null,
    helperId: null,
    stammesId: null,
    groupLeaderId: null,
    valid: false,
  }),
  validations: {},
  computed: {
    total() {
      return (
        this.normal + // eslint-disable-line
        this.helper + // eslint-disable-line
        this.stammes + // eslint-disable-line
        this.groupLeader
      );
    },
    maxHelper() {
      return (
        this.total - // eslint-disable-line
        this.stammes - // eslint-disable-line
        this.groupLeader
      );
    },
    maxStammes() {
      return (
        this.total - // eslint-disable-line
        this.helper - // eslint-disable-line
        this.groupLeader
      );
    },
    maxGroupLeader() {
      return (
        this.total - this.helper - this.stammes
      );
    },
  },
  methods: {
    validate() {},
    prevStep() {
      this.$emit('prevStep');
    },
    nextStep() {
      this.validate();
      if (!this.valid) {
        return;
      }

      this.saveData();
    },
    beforeTabShow() {
      this.loadData();
    },
    loadData() {
      this.isLoading = true;
      Promise.all([this.getParticipant()])
        .then((values) => {
          this.processData(values[0]);
          this.isLoading = false;
        })
        .catch((error) => {
          console.log(error);
          this.isLoading = false;
        });
    },
    async getParticipant() {
      const registrationId = this.$route.params.id;
      const res = await axios.get(
        `${
          this.API_URL
        }basic/participant-group/?registration=${registrationId}&timestamp=${new Date().getTime()}`,
      );
      return res.data;
    },
    processData(items) {
      const obj1 = items.filter((item) => item.participantRole === 1);
      if (obj1 && obj1.length) {
        this.normalId = obj1[0].id;
        this.normal = obj1[0].numberOfPersons;
      } else {
        this.normalId = null;
      }

      const obj2 = items.filter((item) => item.participantRole === 2);
      if (obj2 && obj2.length) {
        this.groupLeaderId = obj2[0].id;
        this.groupLeader = obj2[0].numberOfPersons;
      } else {
        this.groupLeaderId = null;
      }

      const obj3 = items.filter((item) => item.participantRole === 3);
      if (obj3 && obj3.length) {
        this.stammesId = obj3[0].id;
        this.stammes = obj3[0].numberOfPersons;
      } else {
        this.stammesId = null;
      }

      const obj4 = items.filter((item) => item.participantRole === 4);
      if (obj4 && obj4.length) {
        this.helperId = obj4[0].id;
        this.helper = obj4[0].numberOfPersons;
      } else {
        this.helperId = null;
      }
    },
    saveData() {
      const promises = [];
      const registrationId = this.$route.params.id;
      const myUrl = `${this.API_URL}basic/participant-group/`;

      if (this.normalId !== null) {
        promises.push(
          axios.patch(`${myUrl + this.normalId}/`, {
            id: this.normalId,
            participant_role: 1,
            numberOfPersons: this.normal,
            registration: registrationId,
          }),
        );
      } else {
        promises.push(
          axios.post(myUrl, {
            participant_role: 1,
            numberOfPersons: this.normal,
            registration: registrationId,
          }),
        );
      }
      if (this.groupLeaderId !== null) {
        promises.push(
          axios.patch(`${myUrl + this.groupLeaderId}/`, {
            participant_role: 2,
            numberOfPersons: this.groupLeader,
            registration: registrationId,
          }),
        );
      } else {
        promises.push(
          axios.post(myUrl, {
            participant_role: 2,
            numberOfPersons: this.groupLeader,
            registration: registrationId,
          }),
        );
      }

      if (this.stammesId !== null) {
        promises.push(
          axios.patch(`${myUrl + this.stammesId}/`, {
            participant_role: 3,
            numberOfPersons: this.stammes,
            registration: registrationId,
          }),
        );
      } else {
        promises.push(
          axios.post(myUrl, {
            participant_role: 3,
            numberOfPersons: this.stammes,
            registration: registrationId,
          }),
        );
      }

      if (this.helperId !== null) {
        promises.push(
          axios.patch(`${myUrl + this.helperId}/`, {
            participant_role: 4,
            numberOfPersons: this.helper,
            registration: registrationId,
          }),
        );
      } else {
        promises.push(
          axios.post(myUrl, {
            participant_role: 4,
            numberOfPersons: this.helper,
            registration: registrationId,
          }),
        );
      }

      Promise.all(promises).then(() => {
        this.$emit('nextStep');
      });
    },
  },
};
</script>

<style scoped>
</style>

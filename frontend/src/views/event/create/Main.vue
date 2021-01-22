<template>
  <v-card class="mx-auto top-margin">
    <v-row justify="center">
      <v-stepper
        v-model="currentStep"
        vertical
      >
        <template v-for="(step, index) in steps">
          <v-stepper-step
            :key="`stepper-${index}`"
            :complete="currentStep > index+1"
            :step="index+1"
          >
            {{ headerSteps[index] }}
          </v-stepper-step>

          <v-divider :key="index"/>

          <v-stepper-items :key="`stepper-items-${index}`">
            <v-stepper-content
              :step="index+1"
            >
              <component
                :is="step"
                :ref="step.name"
                :position="index+1"
                :max-pos="steps.length"
                @prevStep="prevStep()"
                @nextStep="nextStep()"
                @submit="onCreateEventClick()"
              />
            </v-stepper-content>
          </v-stepper-items>
        </template>
      </v-stepper>
    </v-row>
    <v-snackbar
      v-model="showSuccess"
      color="success"
      y="top"
      :timeout="timeout"
    >
      {{ 'Die Aktion wurde erfolgreich angelegt.' }}
    </v-snackbar>
    <v-snackbar
      v-model="showError"
      color="error"
      y='top'
      :timeout="timeout"
    >
      {{ 'Fehler beim Speichern der Aktion' }}
    </v-snackbar>
  </v-card>
</template>

<script>
import axios from 'axios';

import StepNameDescription from './steps/StepNameDescription.vue';
import StepLocation from './steps/StepLocation.vue';
import StepAgeGroup from './steps/StepAgeGroup.vue';
import StepEventContact from './steps/StepEventContact.vue';
import StepStartEndDeadline from './steps/StepStartEndDeadline.vue';
import StepParticipationFee from './steps/StepParticipationFee.vue';
import StepInvitationCode from './steps/StepInvitationCode.vue';
import StepCrypto from './steps/StepCrypto.vue';

export default {
  components: {
    StepNameDescription,
    StepLocation,
    StepAgeGroup,
    StepEventContact,
    StepStartEndDeadline,
    StepParticipationFee,
    StepInvitationCode,
    StepCrypto,
  },
  data() {
    return {
      API_URL: process.env.VUE_APP_API,
      currentStep: 1,
      showError: false,
      showSuccess: false,
      timeout: 7000,
      data: {
        event: {},
      },
    };
  },
  computed: {
    steps() {
      return [
        StepNameDescription,
        StepInvitationCode,
        StepStartEndDeadline,
        StepLocation,
        StepParticipationFee,
        StepAgeGroup,
        StepCrypto,
        StepEventContact,
      ];
    },
    headerSteps() {
      return [
        'Aktionsbeschreibung',
        'Verifizierungscode',
        'Daten und Uhrzeit',
        'Ort',
        'Teilnehmer_innen Beitrag',
        'Zielgruppe',
        'Verschlüsselung',
        'Kontaktdaten',
      ];
    },
  },
  methods: {
    nextStep() {
      this.currentStep += 1;
    },
    prevStep() {
      this.currentStep -= 1;
    },
    onCreateEventClick() {
      this.handleCreateEventRequest();
    },
    onSuccessfulCreateEvent() {
      setTimeout(() => this.$router.push({ name: 'eventOverview' }), 2000);
    },
    callCreateEventPost() {
      console.log(this.data.event);
      return axios.post(`${this.API_URL}basic/event/`, this.data.event);
    },
    formatCreateEventRequestData() {
      const dataNameDescription = this.$refs.StepNameDescription[0].getData();
      const dataStartEndDeadline = this.$refs.StepStartEndDeadline[0].getData();
      const dataStepLocation = this.$refs.StepLocation[0].getData();
      const dataStepAgeGroup = this.$refs.StepAgeGroup[0].getData();
      const dataStepEventContact = this.$refs.StepEventContact[0].getData();
      const dataStepInvitationCode = this.$refs.StepInvitationCode[0].getData();
      const dataStepParticipationFee = this.$refs.StepParticipationFee[0].getData();
      const dataStepCrypto = this.$refs.StepCrypto[0].getData();

      this.data.event = {
        name: dataNameDescription.name,
        description: dataNameDescription.description,
        location: dataStepLocation.location,
        ageGroups: dataStepAgeGroup.ageGroups,
        contact: dataStepEventContact.contacts,
        startTime: dataStartEndDeadline.startTime,
        endTime: dataStartEndDeadline.endTime,
        registrationDeadline: dataStartEndDeadline.registrationDeadline,
        participationFee: dataStepParticipationFee.participationFee,
        invitationCode: dataStepInvitationCode.invitationCode,
        publicKey: dataStepCrypto.publicKey,
      };
    },
    async handleCreateEventRequest() {
      try {
        this.formatCreateEventRequestData();
        await this.callCreateEventPost();
        this.showSuccess = true;
        this.onSuccessfulCreateEvent();
      } catch (e) {
        console.log(e);
        this.showError = true;
      }
    },
  },
};
</script>

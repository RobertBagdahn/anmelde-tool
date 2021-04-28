<template>
  <v-form ref="formAgeGroup" v-model="valid">
    <v-container>
      <v-row class="mt-6" v-if="!finished">
        <span class="subtitle-1">
          Um eine E-Mail zu versenden geb bitte den E-Mail Code ein
        </span>
      </v-row>
      <v-row class="mt-6" v-else>
        <span class="subtitle-1">
          E-Mail wurde versendet
        </span>
      </v-row>

      <v-row v-if="!finished">
        <v-text-field
          v-model="code"
          :error-messages="codeErrors"
          label="Code"
          required
          @input="validate()"
        />
      </v-row>
      <v-row v-if="!finished">
        <v-checkbox
          v-model="checked"
          :error-messages="checkedErrors"
          label="Ich bin mir sicher"
          required
          @input="validate()"
        />
      </v-row>

      <v-divider class="my-2" />

      <v-btn @click="submit">Absenden</v-btn>
    </v-container>
  </v-form>
</template>

<script>
import { required } from 'vuelidate/lib/validators';
import axios from 'axios';

export default {
  data: () => ({
    items: [],
    code: '',
    checked: false,
    API_URL: process.env.VUE_APP_API,
    valid: true,
    finished: false,
  }),
  validations: {
    code: {
      required,
    },
    checked: {
      required,
    },
  },
  computed: {
    eventId() {
      return this.$route.params.id;
    },
    codeErrors() {
      const errors = [];
      if (!this.$v.code.$dirty) return errors;
      if (!this.$v.code.required) {
        errors.push('Code ist nötig.');
      }
      return errors;
    },
    checkedErrors() {
      const errors = [];
      if (!this.$v.checked.$dirty) return errors;
      if (!this.$v.checked.required) {
        errors.push('Du musst zustimmen.');
      }
      return errors;
    },
  },
  methods: {
    validate() {
      this.$v.$touch();
      this.valid = !this.$v.$error;
    },
    submit() {
      this.validate();
      if (!this.valid) {
        return;
      }
      this.getAgeGroups();
    },
    getAgeGroups() {
      const path = `${this.API_URL}basic/event/${this.eventId}/registration-reminder/?code=${this.code}`;
      axios.post(path).then(() => {
        this.finished = true;
      });
    },
  },
};
</script>

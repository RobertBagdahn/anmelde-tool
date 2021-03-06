<template>
  <v-form ref="formNameDescription" v-model="valid">
    <v-container class="px-0" fluid>
      <v-form>
        <p>
          Gib hier eine Adresse innerhalb Deutschlands an, wo wir ein
          Überraschungspaket für deinen Stamm hinschicken können.
        </p>

        <v-divider class="my-2" />
        <v-subheader> Adresse </v-subheader>
        <v-row>
          <v-col cols="12" sm="6">
            <v-text-field
              v-model="data.firstName"
              :counter="20"
              :error-messages="firstNameErrors"
              label="Vorname*"
              required
              prepend-icon="mdi-card-account-details-outline"
              @input="$v.data.firstName.$touch()"
              @blur="$v.data.firstName.$touch()"
            >
              <template slot="append">
                <v-tooltip bottom>
                  <template v-slot:activator="{ on, attrs }">
                    <v-icon color="success" dark v-bind="attrs" v-on="on">
                      mdi-help-circle-outline
                    </v-icon>
                  </template>
                  <span>
                    {{
                      'Gib hier den Vornamen der Person ein, ' +
                      'die das Paket erhält.'
                    }}
                  </span>
                </v-tooltip>
              </template>
            </v-text-field>
          </v-col>
          <v-col cols="12" sm="6">
            <v-text-field
              v-model="data.lastName"
              :counter="20"
              :error-messages="lastNameErrors"
              label="Nachname*"
              required
              prepend-icon="mdi-card-account-details-outline"
              @input="$v.data.lastName.$touch()"
              @blur="$v.data.lastName.$touch()"
            >
              <template slot="append">
                <v-tooltip bottom>
                  <template v-slot:activator="{ on, attrs }">
                    <v-icon color="success" dark v-bind="attrs" v-on="on">
                      mdi-help-circle-outline
                    </v-icon>
                  </template>
                  <span>
                    {{
                      'Gib hier den Nachnamen der Person ein, ' +
                      'die das Paket erhält.'
                    }}
                  </span>
                </v-tooltip>
              </template>
            </v-text-field>
          </v-col>
        </v-row>
        <v-row>
          <v-col cols="12" sm="6">
            <v-text-field
              v-model="data.street"
              :counter="40"
              :error-messages="streetErrors"
              label="Straße und Hausnummer*"
              prepend-icon="mdi-home"
              required
            >
              <template slot="append">
                <v-tooltip bottom>
                  <template v-slot:activator="{ on, attrs }">
                    <v-icon color="success" dark v-bind="attrs" v-on="on">
                      mdi-help-circle-outline
                    </v-icon>
                  </template>
                  <span>
                    {{
                      'Gib hier die Straße und die Hausnummer der Person ein, ' +
                      'die das Paket erhält.'
                    }}
                  </span>
                </v-tooltip>
              </template>
            </v-text-field>
          </v-col>
          <v-col cols="12" sm="6">
            <v-text-field
              v-model="data.addressAddition"
              :counter="40"
              :error-messages="addressAdditionErrors"
              label="Adresszusatz"
              prepend-icon="mdi-home"
              placeholder="(optional)"
              required
            >
              <template slot="append">
                <v-tooltip bottom>
                  <template v-slot:activator="{ on, attrs }">
                    <v-icon color="success" dark v-bind="attrs" v-on="on">
                      mdi-help-circle-outline
                    </v-icon>
                  </template>
                  <span>
                    {{
                      'Gib hier den Adresszusatz und die ' +
                      'Hausnummer der Person ein, ' +
                      'die das Paket erhält.'
                    }}
                  </span>
                </v-tooltip>
              </template>
            </v-text-field>
          </v-col>
          <v-col cols="12" sm="6">
            <v-autocomplete
              v-model="data.zipCode"
              :items="zipCodeResponse"
              :no-data-text="noZipCodeData"
              no-filter
              :item-text="customText"
              required
              :error-messages="zipCodeErrors"
              item-value="id"
              label="Stadt / Postleitzahl*"
              placeholder="Wähle Stadt oder Postleitzahl"
              :loading="isZipLoading"
              :search-input.sync="search"
              prepend-icon="mdi-city"
            >
              <template slot="append">
                <v-tooltip bottom>
                  <template v-slot:activator="{ on, attrs }">
                    <v-icon color="success" dark v-bind="attrs" v-on="on">
                      mdi-help-circle-outline
                    </v-icon>
                  </template>
                  <span>
                    {{
                      'Trage bitte den Wohnort oder die Postleitzahl ' +
                      'des Wohnorts ein und wähle die richtige Option aus.'
                    }}
                  </span>
                </v-tooltip>
              </template>
            </v-autocomplete>
          </v-col>
        </v-row>
      </v-form>
      <v-divider class="my-3" />

      <prev-next-buttons
        :position="position"
        :max-pos="maxPos"
        @nextStep="nextStep()"
        @prevStep="prevStep"
        @submitStep="submitStep()"
      />
    </v-container>
    <create-location-dialog ref="newLocationDialog" @close="onCloseWindow()" />
  </v-form>
</template>

<script>
import axios from 'axios';
import { required, minLength, maxLength } from 'vuelidate/lib/validators';

import CreateLocationDialog from '@/views/event/create/components/dialog/CreateLocationDialog.vue';
import PrevNextButtons from '../components/button/PrevNextButtonsSteps.vue';

export default {
  name: 'StepBdpDpvPackage',
  displayName: 'Paketadresse',
  props: ['position', 'maxPos'],
  components: {
    PrevNextButtons,
    CreateLocationDialog,
  },
  data: () => ({
    API_URL: process.env.VUE_APP_API,
    valid: true,
    search: null,
    isZipLoading: false,
    zipCodeResponse: [],
    tooMuchData: false,
    data: {
      firstName: null,
      lastName: null,
      street: null,
      addressAddition: null,
      zipCode: null,
      registration: null,
    },
  }),
  validations: {
    data: {
      firstName: {
        required,
        minLength: minLength(2),
        maxLength: maxLength(20),
      },
      lastName: {
        required,
        minLength: minLength(2),
        maxLength: maxLength(20),
      },
      street: {
        required,
        minLength: minLength(5),
        maxLength: maxLength(30),
      },
      zipCode: {
        required,
        minLength: minLength(1),
      },
      addressAddition: {
        maxLength: maxLength(30),
      },
    },
  },
  computed: {
    firstNameErrors() {
      const errors = [];
      if (!this.$v.data.firstName.$dirty) return errors;
      if (!this.$v.data.firstName.required) {
        errors.push('Vorname ist erforderlich.');
      }
      if (!this.$v.data.firstName.minLength) {
        errors.push('Vorname muss mindestens 2 Zeichen lang sein.');
      }
      if (!this.$v.data.firstName.maxLength) {
        errors.push('Vorname darf maximal 20 Zeichen lang sein.');
      }
      return errors;
    },
    lastNameErrors() {
      const errors = [];
      if (!this.$v.data.lastName.$dirty) return errors;
      if (!this.$v.data.lastName.required) {
        errors.push('Nachname ist erforderlich.');
      }
      if (!this.$v.data.lastName.minLength) {
        errors.push('Nachname muss mindestens 2 Zeichen lang sein.');
      }
      if (!this.$v.data.lastName.maxLength) {
        errors.push('Nachname darf maximal 20 Zeichen lang sein.');
      }
      return errors;
    },
    streetErrors() {
      const errors = [];
      if (!this.$v.data.street.$dirty) return errors;
      if (!this.$v.data.street.required) {
        errors.push('Adresse ist erforderlich.');
      }
      if (!this.$v.data.street.minLength) {
        errors.push('Adresse muss mindestens 5 Zeichen lang sein.');
      }
      if (!this.$v.data.street.maxLength) {
        errors.push('Adresse darf maximal 30 Zeichen lang sein.');
      }
      return errors;
    },
    zipCodeErrors() {
      const errors = [];
      if (!this.$v.data.zipCode.$dirty) return errors;

      if (!this.$v.data.zipCode.minLength) {
        errors.push('Stadt ist erforderlich.');
      }

      if (!this.$v.data.zipCode.required) {
        errors.push('Stadt ist erforderlich.');
      }
      return errors;
    },
    addressAdditionErrors() {
      const errors = [];
      if (!this.$v.data.addressAddition.$dirty) return errors;

      // eslint-disable-next-line
      !this.$v.data.addressAddition.maxLength &&
        errors.push('Darf nicht mehr als 20 Zeichen haben');
      return errors;
    },
    noZipCodeData() {
      if (this.tooMuchData) {
        return 'Zu viele Treffer. Suche weiter eingrenzen.';
      }
      return 'Keine Treffer gefunden.';
    },
  },
  watch: {
    postalAddress(value) {
      this.data = value;
    },
    search(searchString) {
      // still loading
      if (this.isZipLoading) return;
      this.tooMuchData = false;
      if (!searchString) return;

      if (searchString.indexOf(' ') >= 0) return;

      if (searchString && searchString.length <= 1) return;

      this.isZipLoading = true;

      this.getZipCodeMapping(searchString)
        .then((res) => {
          this.zipCodeResponse = res;
        })
        .catch((err) => {
          if (err.response.status === 403) {
            this.tooMuchData = true;
            this.zipCodeResponse = [];
          }
          console.log(err.response.status);
        })
        .finally(() => {
          this.isZipLoading = false;
        });
    },
  },
  methods: {
    customText: (item) => `${item.zipCode} — ${item.city}`,
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
      this.savePostalAddress();
    },
    savePostalAddress() {
      this.data.registration = this.$route.params.id;

      if (this.data.id) {
        this.putPostalAddress().then(() => {
          this.$emit('nextStep');
        });
      } else {
        this.postPostalAddress().then(() => {
          this.$emit('nextStep');
        });
      }
    },
    beforeTabShow() {
      this.loadData();
    },
    async getPostalAddress() {
      const registrationId = this.$route.params.id;
      const res = await axios.get(
        `${process.env.VUE_APP_API}basic/postal-address/?registration=${registrationId}`,
      );
      return res.data;
    },
    async postPostalAddress() {
      const res = await axios.post(
        `${process.env.VUE_APP_API}basic/postal-address/`,
        this.data,
      );
      return res.data;
    },
    async putPostalAddress() {
      const id = this.data.id; // eslint-disable-line
      const res = await axios.put(
        `${process.env.VUE_APP_API}basic/postal-address/${id}/`,
        this.data,
      );
      return res.data;
    },
    async getZipCodeMapping(searchString) {
      const path = `${this.API_URL}basic/zip-code/?zip_city=${searchString}`;
      const response = await axios.get(path);

      return response.data;
    },
    loadData() {
      Promise.all([this.getPostalAddress()])
        .then((values) => {
          if (values[0] && values[0].length) {
            this.data = values[0][0]; // eslint-disable-line
            Promise.all([this.getZipCodeById(this.data.zipCode)])
              .then((values2) => {
                [this.zipCodeResponse] = values2;
              })
              .catch((error) => {
                console.log(error);
              });
          }
        })
        .catch((error) => {
          console.log(error);
        });
    },
    async getZipCodeById(id) {
      const path = `${this.API_URL}basic/zip-code/${id}/`;
      const response = await axios.get(path);

      return response.data;
    },
  },
};
</script>

<style>
</style>

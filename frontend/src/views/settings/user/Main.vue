<template>
  <v-form ref="settingsUser">
    <v-container class="top-margin">
      <v-row justify="center">
        <v-flex ma-3 lg9>
          <v-layout column>
            <v-card>
              <v-card-title class="text-center justify-center py-6">
                Hier kannst du deinen persönlichen Account anpassen.
              </v-card-title>
              <v-card-text>
                <v-container>
                  <v-subheader class="ma-5">
                    Hier musst du deine persönlichen Daten angeben. Deine Stammes-Zugehörigkeit
                    sowie deinen Fahrtenname sind wichtig, damit du dich oder deinen Stamm bei
                    Fahrten anmelden kannst. Fülle die Felder deswegen unbedingt
                    aus. Die Handynummer ist freiwillig und hilft dich zu
                    kontaktieren.
                  </v-subheader>
                  <v-row>
                    <v-col cols="12" sm="6">
                      <v-text-field
                        v-model="scoutName"
                        label="Fahrtenname*"
                        prepend-icon="mdi-account-circle"
                        @change="updateData"
                        :error-messages="scoutNameErrors"
                      >
                        <template slot="append">
                          <v-tooltip bottom>
                            <template v-slot:activator="{ on, attrs }">
                              <v-icon
                                color="success"
                                dark
                                v-bind="attrs"
                                v-on="on"
                              >
                                mdi-help-circle-outline
                              </v-icon>
                            </template>
                            <span>
                              {{ tooltip.scoutName }}
                            </span>
                          </v-tooltip>
                        </template>
                      </v-text-field>
                    </v-col>
                    <v-col cols="12" sm="6">
                      <v-text-field
                        readonly
                        disabled
                        filled
                        v-model="email"
                        label="E-Mail Adresse*"
                        prepend-icon="mdi-email"
                      >
                        <template slot="append">
                          <v-tooltip bottom>
                            <template v-slot:activator="{ on, attrs }">
                              <v-icon
                                color="success"
                                dark
                                v-bind="attrs"
                                v-on="on"
                              >
                                mdi-help-circle-outline
                              </v-icon>
                            </template>
                            <span>
                              {{ tooltip.email }}
                            </span>
                          </v-tooltip>
                        </template>
                      </v-text-field>
                    </v-col>
                    <v-col cols="12" sm="6">
                      <v-text-field
                        readonly
                        disabled
                        filled
                        v-model="getStammName"
                        label="Mein Stamm*"
                        prepend-icon="mdi-account-group"
                        :error-messages="stammErrors"
                      >
                        <template slot="append">
                          <v-btn icon @click="onPickStammClick">
                            <v-icon>mdi-pencil</v-icon>
                          </v-btn>
                          <v-tooltip bottom>
                            <template v-slot:activator="{ on, attrs }">
                              <v-icon
                                color="success"
                                dark
                                v-bind="attrs"
                                v-on="on"
                              >
                                mdi-help-circle-outline
                              </v-icon>
                            </template>
                            <span>
                              {{ tooltip.scoutOrganisation }}
                            </span>
                          </v-tooltip>
                        </template>
                      </v-text-field>
                      <pick-stamm-form
                        ref="pickStamm"
                        @sendIdToParent="tranferId"
                      />
                    </v-col>
                    <v-col cols="12" sm="6">
                      <v-text-field
                        v-model="mobileNumber"
                        label="Handynummer"
                        prepend-icon="mdi-cellphone-android"
                        @change="updateData"
                        :error-messages="mobileNumberErrors"
                      >
                        <template slot="append">
                          <v-tooltip bottom>
                            <template v-slot:activator="{ on, attrs }">
                              <v-icon
                                color="success"
                                dark
                                v-bind="attrs"
                                v-on="on"
                              >
                                mdi-help-circle-outline
                              </v-icon>
                            </template>
                            <span>
                              {{ tooltip.mobileNumber }}
                            </span>
                          </v-tooltip>
                        </template>
                      </v-text-field>
                    </v-col>
                    <v-col cols="12">
                        <router-link
                        to="/datenschutz"
                        target="_blank"
                        >
                          Link zur Datenschutzerklärung
                        </router-link>
                    </v-col>
                    <v-col cols="12">
                      <v-checkbox
                        v-model="checkbox"
                        label="Ich habe die Datenschutzerklärung gelesen und akzeptiert!"
                        required
                        :error-messages="checkboxErrors"
                      ></v-checkbox>
                    </v-col>
                  </v-row>
                </v-container>
              </v-card-text>

              <v-card-actions>
                <v-container>
                  <v-row>
                    <v-col cols="12" sm="6" md="4">
                      <v-btn color="success" @click="onSaveClicked">
                        <v-icon left dark>mdi-check</v-icon>
                        Änderungen speichern
                      </v-btn>
                    </v-col>
                    <!-- TODO: add user-delete service and activate button -->
                    <!-- <v-col cols="12" sm="6" md="4">
                      <v-btn dark color="red">
                        <v-icon left>mdi-delete</v-icon>
                        Meine persönlichen Daten löschen.
                      </v-btn>
                    </v-col> -->
                  </v-row>
                </v-container>
              </v-card-actions>
            </v-card>
          </v-layout>
        </v-flex>
      </v-row>
    </v-container>
  </v-form>
</template>

<script>
import axios from 'axios';
import { mapGetters } from 'vuex';
import { validationMixin } from 'vuelidate';
import { required, minLength, maxLength } from 'vuelidate/lib/validators';

import PickStammForm from './form/PickStamm.vue';

export default {
  mixins: [validationMixin],
  components: {
    PickStammForm,
  },
  validations: {
    scoutOrganisation: {
      required,
    },
    mobileNumber: {
      minLength: minLength(6),
      maxLength: maxLength(20),
    },
    scoutName: {
      required,
      maxLength: maxLength(20),
    },
    checkbox: {
      checked(val) {
        return val;
      },
    },
  },
  data() {
    return {
      API_URL: process.env.VUE_APP_API,
      loading: false,
      tooltip: {
        scoutName: 'Gib hier bitte deinen Namen oder deinen Fahrtennamen ein.',
        email:
          'Die E-Mail nutzen wir für die Kommunikation mit dem Tool und für Rückfragen.',
        mobileNumber:
          'Die Handynummer ist freiwillig und hilft dich zu kontaktieren (Für manche Fahrten ist sie Pflicht)',
        scoutOrganisation: 'Mit dem Stift kannst du deinen Stamm auswählen.',
      },
      user: null,
      scoutOrganisation: null,
      mobileNumber: '',
      scoutName: null,
      checkbox: false,
    };
  },
  computed: {
    ...mapGetters(['isAuthenticated', 'getJwtData', 'hierarchyMapping']),
    email() {
      return this.getJwtData.email;
    },
    getStammName() {
      const obj = this.hierarchyMapping.find(
        (user) => user.id === this.scoutOrganisation,
      );
      if (obj && obj.name) {
        return obj.name;
      }
      return 'Noch kein Stamm gewählt';
    },
    checkboxErrors() {
      const errors = [];
      if (!this.$v.checkbox.$dirty) return errors;
      // eslint-disable-next-line
      !this.$v.checkbox.checked &&
        errors.push('Du musst den Datenschutzbestimmungen zustimmen.');
      return errors;
    },
    mobileNumberErrors() {
      const errors = [];
      if (!this.$v.mobileNumber.$dirty) return errors;
      // eslint-disable-next-line
      !this.$v.mobileNumber.maxLength &&
        errors.push('Eine Handynummer hat maxtimal 20 Ziffern');
      // eslint-disable-next-line
      !this.$v.mobileNumber.minLength &&
        errors.push('Eine Handynummer hat mindestens 6 Ziffern.');
      return errors;
    },
    scoutNameErrors() {
      const errors = [];
      if (!this.$v.scoutName.$dirty) return errors;
      // eslint-disable-next-line
      !this.$v.scoutName.maxLength &&
        errors.push('Darf nicht mehr als 20 Zeichen haben');
      // eslint-disable-next-line
      !this.$v.scoutName.required && errors.push('Dein Name ist erforderlich');
      return errors;
    },
    stammErrors() {
      const errors = [];
      if (!this.$v.scoutOrganisation.$dirty) return errors;
      // eslint-disable-next-line
      !this.$v.scoutOrganisation.required &&
        errors.push('Wir brauchen deinen Stamm');
      return errors;
    },
  },
  methods: {
    updateData(type, data) {
      this[type] = data;
    },
    tranferId(id) {
      this.scoutOrganisation = id;
    },
    onPickStammClick() {
      this.$refs.pickStamm.show(this.scoutOrganisation);
    },
    onSaveClicked() {
      this.$v.$touch();
      if (this.$v.$invalid) {
        return;
      }
      this.saveUserData();
    },
    getData() {
      const path = `${this.API_URL}auth/data/user-extended/${this.getJwtData.userId}/`;
      axios
        .get(path)
        .then((res) => {
          this.scoutOrganisation = res.data.scoutOrganisation;
          this.mobileNumber = res.data.mobileNumber;
          this.scoutName = res.data.scoutName;
        })
        .catch(() => {
          console.log('Fehler');
        });
    },
    saveUserData() {
      axios
        .put(
          `${this.API_URL}auth/data/user-extended/${this.getJwtData.userId}/`,
          {
            user: this.getJwtData.userId,
            scoutOrganisation: this.scoutOrganisation,
            mobileNumber: this.mobileNumber,
            scoutName: this.scoutName,
          },
        )
        .then(() => {
          this.showSuccess = true;
          setTimeout(() => this.$router.push({ name: 'eventOverview' }), 100);
        })
        .catch(() => {
          this.showError = true;
        });
    },
  },
  mounted() {
    this.getData();
  },
};
</script>

<template>
  <v-form ref="settingsUser">
    <v-container class="top-margin">
      <v-row justify="center">
        <v-flex ma-3 lg9>
          <v-layout column>
            <v-card>
              <v-card-title class="text-center justify-center py-6">
                Anmeldung starten
              </v-card-title>
              <v-card-text>
                <v-container>
                  <div class="ma-2">
                    <p class="ma-0">
                      Hast du keinen Code bekommen? Schaue nochmal in der
                      Einladung. Falls du nichts findest, melde dich beim
                      Veranstalter, deiner Bundesführung oder bei:
                      <a href="mailto:support@anmelde-tool.de"
                        >support@anmelde-tool.de</a
                      >
                    </p>
                    <p class="mt-4">
                      Bevor deine Anmeldung verbindlich ist, musst du sie im
                      letzten Schritt ausdrücklich bestätigen. Du kannst deinen
                      Anmeldevorgang zu jedem Zeitpunkt abbrechen und später
                      fortsetzen. Deine Daten kannst du bis zum Anmeldeschluss
                      verändern.
                    </p>
                  </div>
                  <v-subheader v-if="isMobilMandatory" class="ma-0">
                    <v-icon class="ma-2" color="error"
                      >mdi-alert-circle
                    </v-icon>
                    Für diese Fahrt ist die Handynummer Pflicht. Falls du sie
                    nicht eintragen hast, kannst du sie nur unter den Profil
                    Einstellungen ändern.
                  </v-subheader>
                  <v-row>
                    <v-col cols="12" sm="6" md="4">
                      <v-text-field
                        v-model="invitationCode"
                        label="Code aus der Einladung"
                        prepend-inner-icon="mdi-lock"
                        :error-messages="invitationCodeErrors"
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
                              {{ tooltip.invitationCode }}
                            </span>
                          </v-tooltip>
                        </template>
                      </v-text-field>
                    </v-col>
                  </v-row>
                  <v-row>
                    <v-col cols="12" sm="6">
                      <v-text-field
                        readonly
                        disabled
                        filled
                        v-model="items.scoutName"
                        label="Mein Name"
                        prepend-inner-icon="mdi-account-circle"
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
                    <v-col cols="12" sm="6" md="4">
                      <v-text-field
                        readonly
                        disabled
                        filled
                        v-model="getStammName"
                        label="Mein Stamm"
                        prepend-inner-icon="mdi-account-group"
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
                              {{ tooltip.stammName }}
                            </span>
                          </v-tooltip>
                        </template>
                      </v-text-field>
                    </v-col>
                    <v-col cols="12" sm="6" md="4">
                      <v-text-field
                        readonly
                        v-if="isMobilMandatory"
                        placeholder="Bitte im Profil hinzufügen"
                        filled
                        v-model="mobileNumber"
                        label="Telefonnummer"
                        prepend-inner-icon="mdi-phone"
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
                  </v-row>
                </v-container>
              </v-card-text>
              <v-card-actions>
                <v-container>
                  <v-row>
                    <v-col cols="12" sm="6" md="4">
                      <v-btn color="success" @click="onSaveClicked">
                        <v-icon left dark>mdi-check</v-icon>
                        Anmeldung starten
                      </v-btn>
                    </v-col>
                  </v-row>
                </v-container>
              </v-card-actions>
            </v-card>
          </v-layout>
        </v-flex>
      </v-row>
      <v-snackbar v-model="showError" color="error" y="top">
        {{ 'Der Code ist falsch' }}
      </v-snackbar>
    </v-container>
  </v-form>
</template>

<script>
import axios from 'axios';
import { mapGetters } from 'vuex';
import { validationMixin } from 'vuelidate';
import { required, requiredIf } from 'vuelidate/lib/validators';

export default {
  mixins: [validationMixin],

  data() {
    return {
      API_URL: process.env.VUE_APP_API,
      loading: false,
      invitationCode: '',
      scoutName: '',
      event: null,
      reg_id: null,
      showError: false,
      items: {},
      tooltip: {
        scoutName:
          'Name falsch? Ändern kannst du deinen Namen nur unter "Profil" (oben rechts)',
        stammName:
          'Stamm falsch? Ändern kannst du deinen Stamm nur unter "Profil" (oben rechts)',
        invitationCode: 'Der Code steht in der offizellen Anmeldung.',
        mobileNumber:
          'Telefonnummer fehlt oder ist falsch? Hinzufügen kannst du deine Nummer nur unter "Profil" (oben rechts)',
      },
    };
  },
  validations: {
    invitationCode: {
      required,
    },
    mobileNumber: {
      required: requiredIf((main) => { // eslint-disable-line
        // eslint-disable-next-line
        return main.isMobilMandatory;
      }),
    },
  },
  props: ['scoutOrganisation'],
  computed: {
    eventId() {
      return this.$route.params.id;
    },
    isMobilMandatory() {
      if (this.event) {
        return this.event.eventTags.filter((tag) => tag === 1).length;
      }
      return false;
    },
    mobileNumber() {
      return this.items.mobileNumber;
    },
    getItems() {
      return this.items;
    },
    ...mapGetters(['isAuthenticated', 'getJwtData', 'hierarchyMapping']),
    email() {
      return this.getJwtData.email;
    },
    getStammName() {
      const obj = this.hierarchyMapping.find(
        (user) => user.id === this.items.scoutOrganisation,
      );
      if (obj && obj.name) {
        return obj.name;
      }
      return 'Kein Stamm';
    },
    getCodeParam() {
      if (this.invitationCode) {
        return this.invitationCode;
      }
      return '';
    },
    invitationCodeErrors() {
      const errors = [];
      if (!this.$v.invitationCode.$dirty) return errors;
      // eslint-disable-next-line
      !this.$v.invitationCode.required &&
        errors.push('Der Einladungscode wird benötigt');
      return errors;
    },
    mobileNumberErrors() {
      const errors = [];
      if (!this.$v.mobileNumber.$dirty) return errors;
      // eslint-disable-next-line
      !this.$v.mobileNumber.required &&
        errors.push('Telefonnummer ist für diese Fahrt verpflichtend. Wechsele ins Profil um die Telefonnummer hinzuzufügen');
      return errors;
    },
  },
  methods: {
    tranferId(id) {
      this.items.scoutOrganisation = id;
    },
    onPickStammClick() {
      this.$refs.pickStamm.show(this.items.scoutOrganisation);
    },
    onSaveClicked() {
      this.$v.$touch();
      if (this.$v.$invalid) {
        return;
      }
      this.createRegestration();
    },
    getData() {
      this.isLoading = true;

      Promise.all([this.loadUserExtended(), this.getEventById(this.eventId)])
        .then((values) => {
          [this.items, this.event] = values;

          // this.$store.commit('setRoleMapping', values[2]);

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
    async getEventById(id) {
      const path = `${process.env.VUE_APP_API}basic/event/${id}/`;
      const response = await axios.get(path);

      return response.data;
    },

    createRegestration() {
      axios
        .post(`${this.API_URL}basic/registration/?code=${this.getCodeParam}`, {
          responsiblePersons: [this.getJwtData.email],
          scoutOrganisation: this.items.scoutOrganisation,
          event: this.eventId,
        })
        .then((response) => {
          this.$router.push({
            name: 'registrationCreate',
            params: {
              id: response.data.id,
              event: response.data.event,
              scoutOrganisation: this.items.scoutOrganisation,
            },
          });
        })
        .catch(() => {
          this.showError = true;
          console.log('Fehler');
        });
    },
  },
  created() {
    this.getData();
  },
};
</script>

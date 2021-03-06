<template>
  <v-dialog
    ref="deadlineDateDialog"
    v-model="active"
    transition="dialog-top-transition"
    fullscreen
  >
    <v-card>
      <v-toolbar dark color="primary">
        <v-btn icon dark @click="active = false">
          <v-icon>mdi-close</v-icon>
        </v-btn>
        <v-toolbar-title>Teilnehmer_innen hinzufügen</v-toolbar-title>
        <v-spacer></v-spacer>
      </v-toolbar>
      <v-container>
        <v-subheader class="ma-5">
          Ich melde folgende_n Teilnehmer_in an.
        </v-subheader>
        <v-form v-model="valid">
          <v-divider />
          <v-subheader> Namen </v-subheader>
          <v-row>
            <v-col cols="12" sm="6" md="4">
              <v-text-field
                v-model="data.firstName"
                :counter="20"
                :error-messages="firstNameErrors"
                label="Vorname"
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
                        'Trage bitte den Vornamen des_der Teilnehmer_in ' +
                        'ein. Zweitnamen müssen nicht mit angegeben werden.'
                      }}
                    </span>
                  </v-tooltip>
                </template>
              </v-text-field>
            </v-col>
            <v-col cols="12" sm="6" md="4">
              <v-text-field
                v-model="data.lastName"
                :counter="20"
                :error-messages="lastNameErrors"
                label="Nachname"
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
                      {{ 'Trage bitte den vollständigen Nachnamen ein.' }}
                    </span>
                  </v-tooltip>
                </template>
              </v-text-field>
            </v-col>
            <v-col cols="12" sm="6" md="4">
              <v-text-field
                v-model="data.scoutName"
                autofocus
                :counter="20"
                :error-messages="scoutNameErrors"
                label="Fahrtenname (optional)"
                required
                prepend-icon="mdi-campfire"
                @input="$v.data.scoutName.$touch()"
                @blur="$v.data.scoutName.$touch()"
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
                        'Trage bitte den Fahrtennamen ' +
                        'des_der Teilnehmer_in ein.'
                      }}
                    </span>
                  </v-tooltip>
                </template>
              </v-text-field>
            </v-col>
          </v-row>

          <v-divider class="my-3" />
          <v-subheader> Alter / Gruppe </v-subheader>
          <v-row>
            <v-col cols="12" sm="6" md="4">
              <v-text-field
                v-model="data.age"
                :error-messages="ageErrors"
                label="Alter zum Fahrtenbeginn"
                suffix="Jahre"
                prepend-icon="mdi-human-child"
                required
                @input="$v.data.age.$touch()"
                @blur="$v.data.age.$touch()"
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
                        'Trage bitte das Alter des_der Teilnehmer_in ' +
                        'zum Start der Fahrt ein (4. bzw. 7. August 2021).'
                      }}
                    </span>
                  </v-tooltip>
                </template>
              </v-text-field>
            </v-col>
            <v-col cols="12" sm="6" md="4">
              <v-combobox
                v-model="data.scoutGroup"
                :items="scoutHierarchyGroups"
                :error-messages="scoutGroupsErrors"
                item-text="name"
                item-value="name"
                required
                :rules="[requiredField, validScoutGroup]"
                label="Gruppe"
                prepend-icon="mdi-account-group"
                @input="$v.data.scoutGroup.$touch()"
                @blur="$v.data.scoutGroup.$touch()"
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
                        'Bitte gib die zugehörige Gruppe zu deinem_r ' +
                        'Teilnehmer_in an. Wähle dazu ' +
                        'eine vorhandene Gruppe aus der Liste aus oder trage den ' +
                        'Gruppennamen in das Feld ein.'
                      }}
                    </span>
                  </v-tooltip>
                </template>
              </v-combobox>
            </v-col>
            <v-col cols="12" sm="6" md="4">
              <v-switch
                v-model="data.isGroupLeader"
                label="Teil der Gruppenführung"
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
                        'Bitte aktiviere die Option, ' +
                        'wenn dein_e Teilnehmer_in ' +
                        'Gruppenführer_in/-leiter_in, Gruppenhelfer_in ' +
                        'oder ähnliches ist.'
                      }}
                    </span>
                  </v-tooltip>
                </template>
              </v-switch>
            </v-col>
          </v-row>

          <v-divider />
          <v-subheader> Adresse / Telefon </v-subheader>
          <v-row>
            <v-col cols="12" sm="6" md="4">
              <v-text-field
                v-model="data.street"
                :counter="40"
                :error-messages="streetErrors"
                label="Straße und Hausnummer"
                prepend-icon="mdi-home"
                required
                @input="$v.data.street.$touch()"
                @blur="$v.data.street.$touch()"
              >
                <template slot="append">
                  <v-tooltip bottom>
                    <template v-slot:activator="{ on, attrs }">
                      <v-icon color="success" dark v-bind="attrs" v-on="on">
                        mdi-help-circle-outline
                      </v-icon>
                    </template>
                    <span>
                      {{ 'Trage bitte Straße und Hausnummer ein.' }}
                    </span>
                  </v-tooltip>
                </template>
              </v-text-field>
            </v-col>
            <v-col cols="12" sm="6" md="4">
              <v-autocomplete
                v-model="data.zipCode"
                :items="zipCodeMapping"
                :item-text="customText"
                required
                :error-messages="zipCodeErrors"
                item-value="id"
                label="Stadt / Postleitzahl"
                placeholder="Wähle Stadt oder Postleitzahl."
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
            <v-col cols="12" sm="6" md="4">
              <v-text-field
                v-model="data.phoneNumber"
                :counter="30"
                :error-messages="phoneNumberErrors"
                label="Telefonnummer"
                prepend-icon="mdi-phone"
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
                        'Trage bitte eine Mobil- oder Festnetznummer ' +
                        'ein unter der der_die Teilnehmer_in oder die ' +
                        'Erziehungsberechtigten nach ' +
                        'der Fahrt erreichbar sind.'
                      }}
                    </span>
                  </v-tooltip>
                </template>
              </v-text-field>
            </v-col>
          </v-row>

          <v-divider />
          <v-subheader>
            Essgewohnheiten / Allergien und Unverträglichkeiten
          </v-subheader>
          <v-row>
            <v-col cols="12" sm="6">
              <v-autocomplete
                v-model="data.eatHabitType"
                :items="eatHabitTypeMapping"
                label="Essgewohnheiten / Allergien und Unverträglichkeiten"
                item-text="name"
                item-value="name"
                prepend-icon="mdi-food"
                multiple
                clearable
                chips
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
                        'Bitte wähle aus den angezeigten Essgewohnheiten. ' +
                        'Weitere Essgewohnheiten können einfach durch Eingabe ' +
                        'im Feld angegeben werden.'
                      }}
                    </span>
                  </v-tooltip>
                </template>
              </v-autocomplete>
            </v-col>
            <v-col cols="12" sm="6">
              <v-combobox
                v-model="eatHabitText"
                v-show="!isEditWindow"
                :error-messages="eatHabitTypeErrors"
                label="weitere Allergien und Unverträglichkeiten (Freitext)"
                prepend-icon="mdi-food"
                clearable
                multiple
                chips
                @input="$v.eatHabitText.$touch()"
                @blur="$v.eatHabitText.$touch()"
              >
                <template slot="append">
                  <v-tooltip bottom>
                    <template v-slot:activator="{ on, attrs }">
                      <v-icon color="success" dark v-bind="attrs" v-on="on">
                        mdi-help-circle-outline
                      </v-icon>
                    </template>
                    <span>
                      {{ 'Trage bitte hier ein, auf welche ' +
                      'Besonderheiten die Küche noch achten soll. ' +
                      'Trage hier nur etwas ein, wenn die Optionen ' +
                      'des anderen Feldes nicht ausreichen' }}
                    </span>
                  </v-tooltip>
                </template>
              </v-combobox>
            </v-col>
          </v-row>
          <v-divider />
          <v-subheader>
            Teilnahme
          </v-subheader>
          <v-row>
            <v-col cols="12" sm="6">
              <v-container fluid>
                <v-switch v-model="isDayGuest" label="Tagesgast?">
                  <template slot="append">
                    <v-tooltip bottom>
                      <template v-slot:activator="{ on, attrs }">
                        <v-icon color="success" dark v-bind="attrs" v-on="on">
                          mdi-help-circle-outline
                        </v-icon>
                      </template>
                      <span>
                        {{ 'Tagesgast?' }}
                      </span>
                    </v-tooltip>
                  </template>
                </v-switch>
                <v-select
                  v-model="data.participantRole"
                  prepend-icon="mdi-tent"
                  :items="getRoleItems"
                  :error-messages="participantRoleErrors"
                  item-text="name"
                  item-value="id"
                  :label="getParticipantRoleLabel"
                  required
                  @input="$v.data.participantRole.$touch()"
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
                          'An welchen Teilfahrten nimmt der Teilnehmende teil?'
                        }}
                      </span>
                    </v-tooltip>
                  </template>
                </v-select>
              </v-container>
            </v-col>
          </v-row>
          <v-divider class="my-3" />
          <v-btn color="primary" @click="onClickOkay"> Speichern </v-btn>
        </v-form>
      </v-container>
      <v-divider class="my-4" />

      <v-snackbar v-model="showError" color="error" y="top" :timeout="timeout">
        {{ 'Fehler beim Anlegen eines Teilnehmenden' }}
      </v-snackbar>
    </v-card>
  </v-dialog>
</template>

<script>
import {
  required,
  minLength,
  maxLength,
  integer,
  minValue,
} from 'vuelidate/lib/validators';
import axios from 'axios';
// import moment from 'moment';
import { mapGetters } from 'vuex';

const scoutGroupStartValidator = (groupObjOrGroupName) => {
  const validStarts = ['Meute', 'Sippe', 'Roverrunde'];
  if (!groupObjOrGroupName) {
    return false;
  }
  const name = groupObjOrGroupName.name
    ? groupObjOrGroupName.name
    : groupObjOrGroupName;
  return validStarts.includes(name.trim().split(' ')[0]);
};

const eatHabitStartValidator = (habit) => {
  if (!habit) {
    return false;
  }
  let oneFalse = 0;
  habit.forEach((h) => {
    if (!h.startsWith('Kein')) oneFalse += 1;
    return oneFalse;
  });
  return oneFalse === 0;
};

const phoneNumStartValidator = (number) => {
  if (!number) return false;
  return number.startsWith('0');
};

export default {
  props: ['isOpen'],
  data: () => ({
    API_URL: process.env.VUE_APP_API,
    active: false,
    valid: true,
    scoutHierarchyGroups: [],
    eatHabitTypeMapping: [],
    isLoading: true,
    isEditWindow: false,
    eatHabitText: [],
    isDayGuest: false,
    data: {
      firstName: null,
      lastName: null,
      street: null,
      zipCode: null,
      phoneNumber: null,
      age: null,
      registration: null,
      eatHabitType: [],
      scoutGroup: null,
      isGroupLeader: false,
      participantRole: 5,
    },
    roleItems: [
      {
        id: 5,
        name: 'Mosaikersleben',
        dayGuest: true,
      },
      {
        id: 6,
        name: 'Kaperfahrt + Mosaikersleben',
        dayGuest: true,
      },
      {
        name: 'Sonntag, 08.08.',
        id: 7,
        dayGuest: false,
      },
      {
        name: 'Sonntag, 08.08. mit Übernachtung',
        id: 10,
        dayGuest: false,
      },
      {
        name: 'Montag, 09.08.',
        id: 8,
        dayGuest: false,
      },
      {
        name: 'Dienstag, 10.08.',
        id: 9,
        dayGuest: false,
      },
      {
        name: 'Montag, 09.08. mit Übernachtung',
        id: 11,
        dayGuest: false,
      },
    ],
    showError: false,
    showSuccess: false,
    timeout: 7000,
  }),
  validations: {
    data: {
      scoutName: {
        minLength: minLength(2),
        maxLength: maxLength(20),
      },
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
      scoutGroup: {
        required,
        scoutGroupStartValidator,
      },
      phoneNumber: {
        required,
        integer,
        minValue: minValue(1),
        phoneNumStartValidator,
      },
      age: {
        required,
        integer,
        minValue: minValue(1),
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
      participantRole: {
        required,
      },
    },
    eatHabitText: {
      eatHabitStartValidator,
    },
  },
  computed: {
    ...mapGetters([
      'isAuthenticated',
      'getJwtData',
      'hierarchyMapping',
      'zipCodeMapping',
    ]),
    getParticipantRoleLabel() {
      return this.isDayGuest ? 'Tagesgast: Welcher Tag?' : 'Mosaikersleben und/oder Kaperfahrt';
    },
    getRoleItems() {
      return this.roleItems.filter((item) => item.dayGuest !== this.isDayGuest);
    },
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
    scoutGroupsErrors() {
      const errors = [];
      if (!this.$v.data.scoutGroup.$dirty) return errors;
      if (!this.$v.data.scoutGroup.required) {
        errors.push('Es muss mindestens eine Gruppe ausgewählt werden.');
      }
      if (!this.$v.data.scoutGroup.scoutGroupStartValidator) {
        errors.push(
          'Der Gruppenname muss mit Meute, Sippe oder Roverrunde beginnen.',
        );
      }
      return errors;
    },
    ageErrors() {
      const errors = [];
      if (!this.$v.data.age.$dirty) return errors;
      if (!this.$v.data.age.required) {
        errors.push('Alter ist erforderlich.');
      }
      if (!this.$v.data.age.integer || !this.$v.data.age.minValue) {
        errors.push('Es muss ein gültiges Alter eingetragen werden.');
      }
      return errors;
    },
    phoneNumberErrors() {
      const errors = [];
      if (!this.$v.data.phoneNumber.$dirty) return errors;
      if (!this.$v.data.phoneNumber.required) {
        errors.push('Telefonnummer ist erforderlich.');
      }
      if (
        !this.$v.data.phoneNumber.integer || // eslint-disable-line
        !this.$v.data.phoneNumber.minValue // eslint-disable-line
      ) {
        errors.push('Telefonnummer darf nur aus Zahlen bestehen.'); // eslint-disable-line
      }
      if (!this.$v.data.phoneNumber.phoneNumStartValidator) {
        errors.push(
          'Die Telefonnummer muss mit 0 beginnen.',
        );
      }
      return errors;
    },
    participantRoleErrors() {
      const errors = [];
      if (!this.$v.data.participantRole.$dirty) return errors;
      if (!this.$v.data.participantRole.required) {
        errors.push('Es muss mindestens eine Fahrt ausgewählt werden.');
      }
      return errors;
    },
    scoutNameErrors() {
      const errors = [];
      if (!this.$v.data.scoutName.$dirty) return errors;
      // eslint-disable-next-line
      !this.$v.data.scoutName.maxLength &&
        errors.push('Darf nicht mehr als 20 Zeichen haben');
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
    eatHabitTypeErrors() {
      const errors = [];
      if (!this.$v.eatHabitText.eatHabitStartValidator) {
        errors.push(
          'Die Essensgewohnheiten müssen mit Kein(e/r) starten.',
        );
      }
      return errors;
    },
  },
  methods: {
    customText: (item) => `${item.zipCode} — ${item.city}`,
    requiredField(value) {
      const errorMsg = 'Dieses Feld muss ausgefüllt werden.';
      if (value instanceof Array && value.length === 0) {
        return errorMsg;
      }
      return !!value || errorMsg;
    },
    validScoutGroup(value) {
      const errorMsg = // eslint-disable-line
        'Der Gruppenname muss mit Meute, Sippe oder Roverrunde beginnen'; // eslint-disable-line
      return !!scoutGroupStartValidator(value) || errorMsg;
    },
    onClickOk() {
      this.active = false;
    },
    onClickCancel() {
      this.active = false;
    },
    openDialog() {
      this.data = {
        firstName: null,
        lastName: null,
        street: null,
        zipCode: null,
        phoneNumber: null,
        age: null,
        registration: null,
        eatHabitType: [],
        scoutGroup: null,
        isGroupLeader: false,
        roles: [],
        participantRole: 5,
      };
      this.eatHabitText = [];
      this.isDayGuest = false;
      this.isEditWindow = false;
      this.active = true;
      this.loadData();
    },
    openDialogEdit(input) {
      this.data = input;
      this.active = true;
      this.isEditWindow = true;
      this.eatHabitText = [];
      this.loadData();
    },
    loadData() {
      this.isLoading = true;

      // eslint-disable-next-line max-len
      Promise.all([this.getGroups(), this.getEatHabitTypeMapping(), this.getZipCodeById(this.data.zipCode)])
        .then((values) => {
          [this.scoutHierarchyGroups, this.eatHabitTypeMapping, this.zipCodeMapping] = values;
          this.isLoading = false;
        })
        .catch((error) => {
          this.errormsg = error.response.data.message;
          this.isLoading = false;
        });
    },
    async getGroups() {
      const path = `${this.API_URL}basic/scout-hierarchy-group/`;
      const response = await axios.get(path);

      return response.data;
    },
    async getEatHabitTypeMapping() {
      const path = `${this.API_URL}basic/eat-habit-type/`;
      const response = await axios.get(path);

      return response.data;
    },
    async getZipCodeById(id) {
      const path = `${this.API_URL}basic/zip-code/${id}/`;
      const response = await axios.get(path);

      return response.data;
    },
    getParticipantPersonalById(id) {
      axios
        .get(`${this.API_URL}basic/participant-personal/${id}/`)
        .then((res) => {
          this.data = res.data;
        })
        .catch((err) => {
          console.log(err);
        });
    },
    closeDialog() {
      this.active = false;
      this.$v.$reset();
      Object.keys(this.data).forEach((key) => {
        this.data[key] = '';
      });
      this.$emit('close');
    },
    validate() {
      this.$v.$touch();
      this.valid = !this.$v.$anyError;
    },
    onClickOkay() {
      this.validate();
      if (this.valid) {
        try {
          this.callCreateParticipantPost();
        } catch (e) {
          console.log(e);
          this.showError = true;
        }
      }
    },
    async callCreateParticipantPost() {
      this.data.registration = this.$route.params.id;
      if (this.data.scoutGroup && this.data.scoutGroup.name) {
        this.data.scoutGroup = this.data.scoutGroup.name;
      }
      if (this.data.eatHabitType && this.data.eatHabitType.name) {
        this.data.eatHabitType = this.data.eatHabitType.name;
      }
      if (this.eatHabitText && this.data.eatHabitType) {
        this.data.eatHabitType = this.data.eatHabitType.concat(
          this.eatHabitText,
        );
      }
      if (!this.data.id) {
        axios
          .post(`${this.API_URL}basic/participant-personal/`, this.data)
          .then(() => {
            this.closeDialog();
            this.$emit('refresh');
          });
      } else {
        axios
          .put(
            `${this.API_URL}basic/participant-personal/${this.data.id}/`,
            this.data,
          )
          .then(() => {
            this.closeDialog();
            this.$emit('refresh');
          });
      }
    },
    getData() {
      return this.data;
    },
  },
};
</script>

<template>
  <v-dialog
    ref="deadlineDateDialog"
    v-model="active"
    transition="dialog-top-transition"
  >
    <v-card>
      <v-toolbar dark color="primary">
        <v-btn icon dark @click="active = false">
          <v-icon>mdi-close</v-icon>
        </v-btn>
        <v-toolbar-title>Haus / Zeltplatz hinzufügen</v-toolbar-title>
        <v-spacer></v-spacer>
      </v-toolbar>
      <v-container>
        <v-form v-model="valid">
          <v-container>
            <v-row>
              <v-col cols="6" sm="6">
                <v-select
                  autofocus
                  :items="event_location_types"
                  item-text="state"
                  item-value="abbr"
                  v-model="data.locationType"
                  required
                  :error-messages="typeErrors"
                  label="Kategorie"
                  prepend-icon="mdi-home"
                >
                </v-select>
              </v-col>
            </v-row>
            <v-row>
              <v-col cols="12" sm="4">
                <v-text-field
                  v-model="data.name"
                  :counter="20"
                  :error-messages="nameErrors"
                  label="Name der Schlafstätte"
                  required
                  prepend-icon="mdi-earth"
                >
                  <template slot="append">
                    <v-tooltip bottom>
                      <template v-slot:activator="{ on, attrs }">
                        <v-icon color="success" dark v-bind="attrs" v-on="on">
                          mdi-help-circle-outline
                        </v-icon>
                      </template>
                      <span>
                        {{ 'Gib hier den Namen der Schlafstätte ein.' }}
                      </span>
                    </v-tooltip>
                  </template>
                </v-text-field>
              </v-col>
              <v-col cols="12" sm="8">
                <v-text-field
                  v-model="data.description"
                  :counter="100"
                  label="Beschreibung/Hinweise zur Schlafstätte"
                  prepend-icon="mdi-card-text"
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
                          'Möchtest du noch etwas hinzufügen? Hast du Anmerkungen?'
                        }}
                      </span>
                    </v-tooltip>
                  </template>
                </v-text-field>
              </v-col>
            </v-row>
            <v-subheader class="my-0"> Anzahl Schlafplätze </v-subheader>
            <v-divider class="my-0" />
            <v-row>
              <v-col cols="12" sm="6">
                <v-text-field
                  v-model="data.capacity"
                  :error-messages="capacityError"
                  label="Anzahl Schlafplätze"
                  prepend-icon="mdi-home"
                >
                  <template slot="append">
                    <v-tooltip bottom>
                      <template v-slot:activator="{ on, attrs }">
                        <v-icon color="success" dark v-bind="attrs" v-on="on">
                          mdi-help-circle-outline
                        </v-icon>
                      </template>
                      <span>
                        {{ 'Wie viele Schlafplätze können dort schlafen?' }}
                      </span>
                    </v-tooltip>
                  </template>
                </v-text-field>
              </v-col>
              <v-col cols="12" sm="6">
                <v-text-field
                  v-model="data.capacityCorona"
                  :error-messages="capacityCoronaError"
                  label="Anzahl Schlafplätze (Corona)"
                  required
                  prepend-icon="mdi-virus"
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
                          'Wie viele Schlafplätze gab es dort im September 2020 ?'
                        }}
                      </span>
                    </v-tooltip>
                  </template>
                </v-text-field>
              </v-col>
            </v-row>
            <v-subheader class="my-0"> Adresse </v-subheader>
            <v-divider class="my-0" />
            <v-row>
              <v-col cols="12" sm="6">
                <v-text-field
                  v-model="data.address"
                  :error-messages="addressErrors"
                  label="Straße und Hausnummer"
                  prepend-icon="mdi-map-marker"
                >
                  <template slot="append">
                    <v-tooltip bottom>
                      <template v-slot:activator="{ on, attrs }">
                        <v-icon color="success" dark v-bind="attrs" v-on="on">
                          mdi-help-circle-outline
                        </v-icon>
                      </template>
                      <span>
                        {{ 'Die genaue Adresse der Schlafstätte.' }}
                      </span>
                    </v-tooltip>
                  </template>
                </v-text-field>
              </v-col>
              <v-col cols="12" sm="6">
                <v-autocomplete
                  v-model="data.zipCode"
                  :items="zipCodeResponse"
                  :item-text="customText"
                  required
                  :error-messages="zipCodeErrors"
                  item-value="id"
                  label="Stadt / Postleitzahl"
                  placeholder="Wähle Stadt oder Postleitzahl."
                  prepend-icon="mdi-city"
                  :loading="isZipLoading"
                  :search-input.sync="search"
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
            <v-subheader class="my-0"> Kosten </v-subheader>
            <v-divider class="my-0" />
            <v-row>
              <v-col cols="12" sm="6">
                <v-text-field
                  v-model="data.perPersonFee"
                  :error-messages="perPersonFeeErrors"
                  :disabled="feeNotKnowen || noCostState"
                  label="Kosten pro Person pro Nacht."
                  prepend-icon="mdi-currency-eur"
                >
                  <template slot="append">
                    <v-tooltip bottom>
                      <template v-slot:activator="{ on, attrs }">
                        <v-icon color="success" dark v-bind="attrs" v-on="on">
                          mdi-help-circle-outline
                        </v-icon>
                      </template>
                      <span>
                        {{ 'Kosten pro Person pro Nacht.' }}
                      </span>
                    </v-tooltip>
                  </template>
                </v-text-field>
              </v-col>
              <v-col cols="12" sm="6">
                <v-text-field
                  v-model="data.fixFee"
                  :disabled="feeNotKnowen || noCostState"
                  :error-messages="fixFeeErrors"
                  label="Fixkosten"
                  prepend-icon="mdi-currency-eur"
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
                          'Gib hier die Fixkosten ein, die für ein ' +
                          'Wochenende entstehen (Strom, Miete, etc.).'
                        }}
                      </span>
                    </v-tooltip>
                  </template>
                </v-text-field>
              </v-col>
              <v-col cols="12" sm="6">
                <v-switch
                  v-model="feeNotKnowen"
                  label="Ich kenne die Preise nicht"
                ></v-switch>
              </v-col>
              <v-col cols="12" sm="6">
                <v-switch
                  v-model="noCostState"
                  label="Es fallen keine Kosten an"
                ></v-switch>
              </v-col>
            </v-row>
            <v-subheader class="my-0">
              Kontakt Haus-/Zeltplatzvermietung
            </v-subheader>
            <v-divider class="my-0" />
            <v-row>
              <v-col cols="12" sm="6" md="4">
                <v-text-field
                  prepend-icon="mdi-account"
                  v-model="data.contactName"
                  :error-messages="contactNameErrors"
                  label="Name der Kontaktperson"
                >
                  <template slot="append">
                    <v-tooltip bottom>
                      <template v-slot:activator="{ on, attrs }">
                        <v-icon color="success" dark v-bind="attrs" v-on="on">
                          mdi-help-circle-outline
                        </v-icon>
                      </template>
                      <span>
                        {{ 'Name der Kontaktperson.' }}
                      </span>
                    </v-tooltip>
                  </template>
                </v-text-field>
              </v-col>
              <v-col cols="12" sm="6" md="4">
                <v-text-field
                  prepend-icon="mdi-at"
                  v-model="data.contactEmail"
                  :error-messages="contactEmailErrors"
                  label="E-Mail"
                >
                  <template slot="append">
                    <v-tooltip bottom>
                      <template v-slot:activator="{ on, attrs }">
                        <v-icon color="success" dark v-bind="attrs" v-on="on">
                          mdi-help-circle-outline
                        </v-icon>
                      </template>
                      <span>
                        {{ 'E-Mail der Kontaktperson.' }}
                      </span>
                    </v-tooltip>
                  </template>
                </v-text-field>
              </v-col>
              <v-col cols="12" sm="6" md="4">
                <v-text-field
                  prepend-icon="mdi-phone"
                  v-model="data.contactPhone"
                  :error-messages="contactPhoneErros"
                  label="Telefonnummer"
                >
                  <template slot="append">
                    <v-tooltip bottom>
                      <template v-slot:activator="{ on, attrs }">
                        <v-icon color="success" dark v-bind="attrs" v-on="on">
                          mdi-help-circle-outline
                        </v-icon>
                      </template>
                      <span>
                        {{ 'Telefonnummer der Kontaktperson.' }}
                      </span>
                    </v-tooltip>
                  </template>
                </v-text-field>
              </v-col>
            </v-row>
          </v-container>
          <v-divider class="my-3" />
          <v-btn color="primary" @click="onClickOkay"> Speichern </v-btn>
        </v-form>
      </v-container>
      <v-divider class="my-4" />

      <v-snackbar v-model="showError" color="error" y="top" :timeout="timeout">
        {{ 'Fehler beim Erstellen des Ortes' }}
      </v-snackbar>
    </v-card>
  </v-dialog>
</template>

<script>
import {
  required,
  minLength,
  numeric,
  requiredIf,
} from 'vuelidate/lib/validators';
import axios from 'axios';

export default {
  props: ['isOpen'],
  data: () => ({
    API_URL: process.env.VUE_APP_API,
    active: false,
    valid: true,
    feeNotKnowen: false,
    event_location_types: [{ state: 'No data. PLS Set data', abbr: 0 }],
    noCostState: false,
    isZipLoading: false,
    zipCodeResponse: [],
    search: null,
    data: {
      name: '',
      locationType: '',
      description: '',
      address: '',
      zipCode: null,
      contactName: '',
      contactEmail: '',
      contactPhone: '',
      capacity: null,
      capacityCorona: null,
      perPersonFee: null,
      fixFee: null,
    },
    showError: false,
    showSuccess: false,
    timeout: 7000,
  }),
  validations: {
    data: {
      locationType: {
        required,
      },
      name: {
        required,
      },
      address: {
        required,
      },
      zipCode: {
        required,
        minLength: minLength(1),
      },
      capacity: {
        required,
        numeric,
      },
      capacityCorona: {
        required,
        numeric,
      },
      perPersonFee: {
        numeric,
      },
      fixFee: {
        numeric,
      },
      contactName: {
        required,
      },
      contactEmail: {
        required: requiredIf((main) => { // eslint-disable-line
          // eslint-disable-next-line
          return !main.contactPhone;
        }),
      },
      contactPhone: {
        required: requiredIf((main) => { // eslint-disable-line
          // eslint-disable-next-line
          return !main.contactEmail;
        }),
      },
    },
  },
  watch: {
    noCostState(value) {
      if (value === true) {
        this.data.perPersonFee = 0;
        this.data.fixFee = 0;
        this.feeNotKnowen = false;
      }
    },
    feeNotKnowen(value) {
      if (value === true) {
        this.data.perPersonFee = null;
        this.data.fixFee = null;
        this.noCostState = false;
      }
    },
    search(searchString) {
      // still loading
      if (this.isZipLoading) return;

      if (!searchString) return;

      if (searchString.indexOf(' ') >= 0) return;

      if (searchString && searchString.length <= 1) return;

      this.isZipLoading = true;

      this.getZipCodeMapping(searchString)
        .then((res) => {
          this.zipCodeResponse = res;
        })
        .catch((err) => {
          console.log(err);
        })
        .finally(() => {
          this.isZipLoading = false;
        });
    },
  },
  computed: {
    capacityError() {
      const errors = [];
      if (!this.$v.data.capacity.$dirty) return errors;
      if (!this.$v.data.capacity.required) {
        errors.push('Ist verpflichtend.');
      }
      if (!this.$v.data.capacity.numeric) {
        errors.push('Muss numerisch sein.');
      }
      return errors;
    },
    perPersonFeeErrors() {
      const errors = [];
      if (!this.$v.data.perPersonFee.$dirty) return errors;
      if (!this.$v.data.perPersonFee.numeric) {
        errors.push('Ist verpflichtend.');
      }
      return errors;
    },
    fixFeeErrors() {
      const errors = [];
      if (!this.$v.data.fixFee.$dirty) return errors;
      if (!this.$v.data.fixFee.numeric) {
        errors.push('Ist verpflichtend.');
      }
      return errors;
    },
    capacityCoronaError() {
      const errors = [];
      if (!this.$v.data.capacityCorona.$dirty) return errors;
      if (!this.$v.data.capacityCorona.required) {
        errors.push('Ist verpflichtend.');
      }
      if (!this.$v.data.capacityCorona.numeric) {
        errors.push('Muss numerisch sein.');
      }
      return errors;
    },
    contactNameErrors() {
      const errors = [];
      if (!this.$v.data.contactName.$dirty) return errors;
      if (!this.$v.data.contactName.required) {
        errors.push('Ist verpflichtend.');
      }
      return errors;
    },
    contactPhoneErros() {
      const errors = [];
      if (!this.$v.data.contactPhone.$dirty) return errors;
      // eslint-disable-next-line
      !this.$v.data.contactPhone.required &&
        errors.push('Telefonnummer oder E-Mail ist verpflichtend');
      return errors;
    },
    contactEmailErrors() {
      const errors = [];
      if (!this.$v.data.contactEmail.$dirty) return errors;
      // eslint-disable-next-line
      !this.$v.data.contactEmail.required &&
        errors.push('Telefonnummer oder E-Mail ist verpflichtend');
      return errors;
    },
    typeErrors() {
      const errors = [];
      if (!this.$v.data.locationType.$dirty) return errors;
      if (!this.$v.data.locationType.required) {
        errors.push('Ist verpflichtend.');
      }
      return errors;
    },
    nameErrors() {
      const errors = [];
      if (!this.$v.data.name.$dirty) return errors;
      if (!this.$v.data.name.required) {
        errors.push('Ist verpflichtend.');
      }
      return errors;
    },
    addressErrors() {
      const errors = [];
      if (!this.$v.data.address.$dirty) return errors;
      if (!this.$v.data.address.required) {
        errors.push('Ist verpflichtend.');
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
  },
  methods: {
    async getZipCodeMapping(searchString) {
      const path = `${this.API_URL}basic/zip-code/?zip_city=${searchString}`;
      const response = await axios.get(path);

      return response.data;
    },
    customText: (item) => `${item.zipCode} — ${item.city}`,
    openDialog() {
      this.active = true;
    },
    openDialogEdit(input) {
      this.data = input;
      this.feeNotKnowen = this.data.fixFee == null && this.data.perPersonFee == null;
      this.active = true;
      this.isEditWindow = true;
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
          this.callCreateEventLocationPost();
          this.closeDialog();
        } catch (e) {
          console.log(e);
          this.showError = true;
        }
      }
    },
    async callCreateEventLocationPost() {
      this.data.registration = this.$route.params.id;
      if (this.feeNotKnowen) {
        this.data.fixFee = null;
        this.data.perPersonFee = null;
      }
      if (this.data.perPersonFee === '') {
        this.data.perPersonFee = null;
      }
      if (this.data.fixFee === '') {
        this.data.fixFee = null;
      }
      if (!this.data.id) {
        axios
          .post(`${this.API_URL}basic/event-location/`, this.data)
          .then(() => {
            this.closeDialog();
            this.$emit('refresh');
          });
      } else {
        axios
          .put(
            `${this.API_URL}basic/event-location/${this.data.id}/`,
            this.data,
          )
          .then(() => {
            this.closeDialog();
            this.$emit('refresh');
          });
      }
    },
  },
};
</script>

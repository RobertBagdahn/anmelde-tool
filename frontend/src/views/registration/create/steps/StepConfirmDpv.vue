<template>
  <v-form ref="formNameDescription" v-model="valid">
    <v-container>
      <v-row class="mt-2">
        <span class="text-left subtitle-1">
          <p><b>Zusammenfassung</b></p>
          <p>
            Hier folgt nun deine Datenübersicht. Bitte vergewissere Dich, dass
            alles richtig ist und klicke anschließend auf Absenden:
          </p>
          <p>
            Du <b>{{ scoutName }}</b> hast <b>{{ scoutOrganisation }}</b>
            für das BdP-DPV stadt&spiel für das Wochenende vom 17.-19.September
            2021 mit insgesamt
            <b>{{ totalParticipants }}</b>
            Teilnehmende angemeldet.
          </p>
        </span>
        <v-expansion-panels accordion>
          <v-expansion-panel>
            <v-expansion-panel-header>
              Verantwortliche Person:
              <b>{{ scoutName }}</b>
            </v-expansion-panel-header>
            <v-expansion-panel-content>
              E-Mail-Adresse:
              <b>{{ email }}</b
              ><br />
              Telefon/Handy (freiwillig):
              <b>{{ phone }} </b><br />
            </v-expansion-panel-content>
          </v-expansion-panel>
          <v-expansion-panel>
            <v-expansion-panel-header>
              Teilnehmende insgesamt:
              <b>{{ totalParticipants }}</b>
            </v-expansion-panel-header>
            <v-expansion-panel-content>
              Das sind die Daten deines Stammes<br />
              <li
                v-for="item in groupParticipants"
                :key="item.participantRoleId"
              >
                {{ item.participantRoleId_Name }}:
                <b>{{ item.registered }}</b>
              </li>
            </v-expansion-panel-content>
          </v-expansion-panel>
          <v-expansion-panel>
            <v-expansion-panel-header>
              Eigene Schlafstätte:
              <b>{{ ownLocationsString }}</b>
            </v-expansion-panel-header>
            <v-expansion-panel-content>
              <v-list>
                <v-list-item-group color="primary">
                  <v-list-item
                    v-for="(item, i) in ownLocations" :key="i"
                  >
                    <v-list-item-content>
                      <v-list-item-title v-text="item.name"></v-list-item-title>
                      <v-list-item-subtitle>
                        Daten des Heims: Adresse: <b>{{ item.address }}</b
                        >, <b>{{ item.zipCode_ZipCode }}</b
                        ><br />
                        Schlafplatzanzahl:<br />
                        - Haus (ohne Corona/mit Corona):
                        <b>{{ item.capacity }}</b
                        >/<b>{{ item.capacityCorona }}</b
                        ><br />
                        Kosten:<br />
                        - Pro Person: <b>{{ item.perPersonFee }}</b> Euro<br />
                        - Fixkosten: <b>{{ item.fixFee }}</b> Euro<br />
                        Die Kontaktperson für Haus/Lagerplatz
                        <b>{{ item.contactName }}</b> ist wie folgt zu
                        erreichen:<br />
                        <b>{{ item.contactEmail }}</b
                        >/<b>{{ item.contactPhone }}</b
                        ><br />
                      </v-list-item-subtitle>
                    </v-list-item-content>
                  </v-list-item>
                </v-list-item-group>
              </v-list>
            </v-expansion-panel-content>
          </v-expansion-panel>
          <v-expansion-panel>
            <v-expansion-panel-header>
              Da wollen wir hin:
              <b>
                <div v-if="customChoice === 1">
                  Hier bleiben
                </div>
                <div
                  v-if="[4, 5, 6].includes(customChoice)"
                >
                  Weg gehen
                </div>
                <div
                  v-if="[7, 8, 9].includes(customChoice)"
                >
                  Beides ok
                </div>
                <div
                  v-if="[10, 11, 12].includes(customChoice)"
                >
                  Weg gehen
                </div>
              </b>
            </v-expansion-panel-header>
            <v-expansion-panel-content>
              Dort geht es für deinen Stamm hin:
              <b>
                <div v-if="customChoice === 1">
                  Wir wollen bei uns im Heim bleiben und besucht werden
                </div>
                <div
                  v-if="[4, 5, 6].includes(customChoice)"
                >
                  Wir wollen einen anderen Stamm besuchen und stellen unser Heim
                  zur Verfügung.
                </div>
                <div
                  v-if="
                    [7, 8, 9].includes(customChoice)
                  "
                >
                  Wir stellen unser Heim zur Verfügung/wir bleiben da, fahren
                  aber auch gerne weg
                </div>
                <div
                  v-if="
                    [10, 11, 12].includes(customChoice)
                  "
                >
                  Wir wollen einen anderen Stamm besuchen.
                </div>
              </b>
            </v-expansion-panel-content>
          </v-expansion-panel>
          <v-expansion-panel>
            <v-expansion-panel-header>
              Zusätzliche Schlafstätten:
              <b>{{ suggestionLocationsString }}</b>
            </v-expansion-panel-header>
            <v-expansion-panel-content>
              Du hast diese zusätzlichen Heime eingetragen mit folgenden Daten:
              <v-list>
                <v-list-item-group color="primary">
                  <v-list-item
                    v-for="(item, i) in suggestionLocations"
                    :key="i"
                  >
                    <v-list-item-content>
                      <v-list-item-title v-text="item.name"></v-list-item-title>
                      <v-list-item-subtitle>
                        Kontakt: <b>{{ item.contactName }}</b> ist zu erreichen
                        unter <b>{{ item.contactEmail }}</b> und/oder
                        <b>{{ item.contactPhone }}</b>
                      </v-list-item-subtitle>
                    </v-list-item-content>
                  </v-list-item>
                </v-list-item-group>
              </v-list>
            </v-expansion-panel-content>
          </v-expansion-panel>
          <!-- <v-expansion-panel>
            <v-expansion-panel-header>
              Paket:
              <b
                >{{
                  currentRegistrationSummary[0].postaladdress[0].firstName
                }}
                -
                {{ currentRegistrationSummary[0].postaladdress[0].lastName }}</b
              >
            </v-expansion-panel-header>
            <v-expansion-panel-content>
              Für ein Paket an deinen Stamm hast Du folgende Adresse angegeben:
              <br />
              <b
                >{{ currentRegistrationSummary[0].postaladdress[0].firstName }}
                {{ currentRegistrationSummary[0].postaladdress[0].lastName }},
                {{ currentRegistrationSummary[0].postaladdress[0].street }},
                {{
                  currentRegistrationSummary[0].postaladdress[0]
                    .zipCode_ZipCode
                }},
                {{
                  currentRegistrationSummary[0].postaladdress[0].addressAddition
                }}
              </b>
            </v-expansion-panel-content>
          </v-expansion-panel> -->
        </v-expansion-panels>
      </v-row>
      <v-divider class="text-left my-2" />
      <v-row>
        <v-checkbox
          v-model="data.checkbox1"
          :label="`Ich habe meine Daten überprüft und melde meinen Stamm verbindlich zur Fahrt an.`"
        >
        </v-checkbox>
      </v-row>

      <v-divider class="my-3" />

      <prev-next-buttons
        :position="position"
        :max-pos="maxPos"
        @nextStep="nextStep()"
        @prevStep="prevStep"
        @submitStep="submitStep()"
      />
    </v-container>
  </v-form>
</template>

<script>
import { required } from 'vuelidate/lib/validators';
import axios from 'axios';
import { mapGetters } from 'vuex';
import PrevNextButtons from '../components/button/PrevNextButtonsSteps.vue';

export default {
  name: 'StepNameDescription',
  displayName: 'Zusammenfassung und Bestätigung',
  props: ['position', 'maxPos'],
  components: {
    PrevNextButtons,
  },
  data: () => ({
    API_URL: process.env.VUE_APP_API,
    valid: true,
    suggestionLocationTypeIds: [3, 4],
    ownLocationTypeIds: [1, 2],
    data: {
      checkbox1: false,
    },
  }),
  validations: {
    data: {
      checkbox1: {
        required,
        checked: (value) => value === true,
      },
    },
  },
  computed: {
    ...mapGetters(['currentRegistrationSummary']),
    id() {
      return this.$route.params.id;
    },
    customChoice() {
      if (this.currentRegistration) {
        return this.currentRegistration.customChoice;
      }
      return null;
    },
    ownLocations() {
      if (this.locationsArray && this.locationsArray.length) {
        return this.locationsArray.filter(
          (item) => this.ownLocationTypeIds.includes(item.locationType_Id),
        );
      }
      return [];
    },
    ownLocationsString() {
      if (this.ownLocations && this.ownLocations.length) {
        return this.ownLocations.map((x) => x.name).join(', ');
      }
      return ['Keine'];
    },
    suggestionLocations() {
      if (this.locationsArray && this.locationsArray.length) {
        return this.locationsArray.filter(
          (item) => this.suggestionLocationTypeIds.includes(item.locationType_Id),
        );
      }
      return [];
    },
    suggestionLocationsString() {
      if (this.suggestionLocations && this.suggestionLocations.length) {
        return this.suggestionLocations.map((x) => x.name).join(', ');
      }
      return ['Keine'];
    },
    currentRegistration() {
      if (
        this.currentRegistrationSummary && // eslint-disable-line
        this.currentRegistrationSummary.length && // eslint-disable-line
        this.currentRegistrationSummary[0]
      ) {
        return this.currentRegistrationSummary[0];
      }
      return null;
    },
    groupParticipants() {
      if (this.currentRegistration) {
        return this.currentRegistration.groupParticipants;
      }
      return [];
    },
    responsiblePersons() {
      if (this.currentRegistration) {
        return this.currentRegistration.responsiblePersons;
      }
      return null;
    },
    scoutName() {
      if (
        this.responsiblePersons && // eslint-disable-line
        this.responsiblePersons.length // eslint-disable-line
      ) {
        return this.responsiblePersons[0].userextended_ScoutName;
      }
      return null;
    },
    scoutOrganisation() {
      return this.currentRegistrationSummary.scoutOrganisation;
    },
    totalParticipants() {
      if (
        this.currentRegistrationSummary && // eslint-disable-line
        this.currentRegistrationSummary.length // eslint-disable-line
      ) {
        return this.currentRegistrationSummary.totalParticipants;
      }
      return null;
    },
    email() {
      if (
        this.responsiblePersons && // eslint-disable-line
        this.responsiblePersons.length // eslint-disable-line
      ) {
        return this.responsiblePersons[0].username;
      }
      return null;
    },
    phone() {
      if (
        this.responsiblePersons && // eslint-disable-line
        this.responsiblePersons.length // eslint-disable-line
      ) {
        return this.responsiblePersons[0].userextended_MobileNumber;
      }
      return null;
    },
    locationsArray() {
      if (
        this.currentRegistrationSummary && // eslint-disable-line
        this.currentRegistrationSummary.length
      ) {
        return this.currentRegistrationSummary[0].locations;
      }
      return [];
    },
  },
  methods: {
    async getRegistrationSummaryData() {
      const path = `${process.env.VUE_APP_API}basic/registration/${this.id}/summary/`;
      axios
        .get(path)
        .then((res) => {
          this.$store.commit('setCurrentRegistrationSummary', res.data);
        })
        .catch(() => {
          console.log('Fehler');
        });
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
    beforeTabShow() {
      this.getRegistrationSummaryData();
    },
  },
};
</script>

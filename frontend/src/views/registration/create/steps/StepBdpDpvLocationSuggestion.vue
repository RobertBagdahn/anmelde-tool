<template>
  <v-form ref="formNameDescription" v-model="valid">
    <v-container class="px-0" fluid>
      <v-container>
        <p>
          Wir würden uns freuen, wenn du noch weitere Heime/Zeltplätze hinzufügst.
          <br>
Wichtig wären uns der Name des Ortes und eine Kontakperson mit EMail oder Telefonnummer.<br>
          Alles andere kannst du freiwillig angeben.
        </p>

        <v-divider class="my-2" />

        <v-btn color="primary" @click="newLocation()">
          Platz oder Haus vorschlagen
        </v-btn>
        <v-list v-if="!isLoading">
          <v-subheader>Orte</v-subheader>
          <v-list-item-group color="primary">
            <v-list-item
              v-for="(item, i) in items"
              :key="i"
            >
              <v-list-item-avatar>
                <v-icon color="black" dark>mdi-home</v-icon>
              </v-list-item-avatar>
              <v-list-item-content>
                <v-list-item-title
                  v-text="item.name"
                ></v-list-item-title>
              </v-list-item-content>
              <v-list-item-action>
                <v-btn dense icon @click="editLocation(item.id)">
                  <v-icon color="primary lighten-1">mdi-pencil</v-icon>
                </v-btn>
              </v-list-item-action>
              <v-list-item-action>
                <v-btn dense icon @click="deleteLocation(item.id)">
                  <v-icon color="red lighten-1">mdi-trash-can</v-icon>
                </v-btn>
              </v-list-item-action>
            </v-list-item>
            <v-list-item
              v-if="!items.length"
            >
              Bisher hast du noch kein Vorschläge hinzugefügt.
            </v-list-item>
          </v-list-item-group>
        </v-list>
        <div v-else>
          <div class="text-center ma-5">
          <p>
            Lade Daten
          </p>
            <v-progress-circular
              :size="80"
              :width="10"
              color="primary"
              indeterminate
            ></v-progress-circular>
          </div>
        </div>
      </v-container>
      <v-divider class="my-3" />

      <prev-next-buttons
        :position="position"
        :max-pos="maxPos"
        @nextStep="nextStep()"
        @prevStep="prevStep"
        @submitStep="submitStep()"
      />
    </v-container>
    <delete-location-modal
      ref="deleteLocationModal"
      @refresh="onRefresh()"
    />
    <create-location-dialog
      ref="newLocationDialog"
      @close="onCloseWindow()"
      @refresh="onRefresh()"
    />
  </v-form>
</template>

<script>
import axios from 'axios';
import CreateLocationDialog from '@/views/event/create/components/dialog/CreateLocationDialog.vue';
import DeleteLocationModal from '@/views/registration/create/steps/dialog/DeleteLocationModal.vue';
import PrevNextButtons from '../components/button/PrevNextButtonsSteps.vue';

export default {
  name: 'StepBdpDpvLocationSuggention',
  displayName: 'Heim-/Zeltplatzvorschläge',
  props: ['position', 'maxPos'],
  components: {
    PrevNextButtons,
    CreateLocationDialog,
    DeleteLocationModal,
  },
  data: () => ({
    API_URL: process.env.VUE_APP_API,
    event_location_types: [
      { state: 'Fremden Zeltplatz vorschlagen', abbr: 3 },
      { state: 'Fremdes Heim vorschlagen', abbr: 4 }],
    show_event_location_types: [3, 4],
    valid: true,
    radioGroup: 0,
    radioGroup2: 0,
    isLoading: true,
    items: [{ locations: [] }],
  }),
  validations: {},
  watch: {
    radioGroup(value) {
      this.$store.commit('setDpvAddedLocation', value === '1');
    },
  },
  methods: {
    newLocation() {
      this.$refs.newLocationDialog.event_location_types = this.event_location_types;
      this.$refs.newLocationDialog.openDialog();
    },
    onCloseWindow() {
      // this.$store.commit('setDpvAddedLocation', true);
    },
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
      this.$emit('nextStep');
    },
    submitStep() {
      this.validate();
      if (!this.valid) {
        return;
      }
      this.$emit('submit');
    },
    getLocations() {
      this.isLoading = true;
      Promise.all([this.loadRegistrationEventLocations()])
        .then((values) => {
          [this.items] = values;
          this.isLoading = false;
          this.items = this.items.filter(
            (item) => this.show_event_location_types.includes(item.locationType),
          );
        })
        .catch((error) => {
          this.errormsg = error.response.data.message;
          this.isLoading = false;
        });
    },
    async loadRegistrationEventLocations() {
      const path = `${this.API_URL}basic/event-location/?registration=${this.$route.params.id}`;
      const response = await axios.get(path);

      return response.data;
    },
    onRefresh() {
      this.getLocations();
    },
    editLocation(id) {
      this.$refs.newLocationDialog.event_location_types = this.event_location_types;
      this.$refs.newLocationDialog.openDialogEdit(
        this.items.filter((i) => i.id === id)[0],
      );
    },
    deleteLocation(item) {
      this.$refs.deleteLocationModal.show(item);
    },
    beforeTabShow() {
      this.onRefresh();
    },
  },
  created() {
    this.$store.commit('setDpvAddedLocation', false);
  },
};
</script>

<style>
</style>

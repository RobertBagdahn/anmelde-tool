<template>
  <div class="pdf-content">
    <template v-for="(group, index) in current">
      <v-card
        v-bind:key="`pdfContent-'${group.name}${index}`"
        class="ml-3 mt-4 d-inline-block"
        :class="(group.verband === 'BdP') ? 'bdp-color' : 'dpv-color'"
        width="370px"
        height="195px"
        outlined
      >
        <v-card-text class="text-truncate">
          <h4> {{ group.scoutOrganisation_Name }} </h4>
          <h5>
            Bund: {{ group.bund }}
            <span v-if="group.bund !== 'BdP'"> ({{ group.verband }})</span>
          </h5>
          <h5>
            <span :class="group.choice"> Ort: {{ group.city }} </span>
          </h5>
          <h5> Teilnehmer: {{ group.participants }} </h5>
        </v-card-text>
      </v-card>
      <div v-if="(index + 1) % 10 === 0" class="html2pdf__page-break"
           v-bind:key="`pdfContent-pageBreak-'${group.name}${index}`"/>
    </template>
  </div>
</template>
<script>
import axios from 'axios';

export default {
  data: () => ({
    API_URL: process.env.VUE_APP_API,
    groupsPerPage: 10,
    groupsPerDocument: 100,
    allGroups: [],
    groupParts: [],
    current: [],
  }),
  computed: {
    eventId() {
      return this.$route.params.id;
    },
  },
  methods: {
    async loadData() {
      const result = await axios.get(`${this.API_URL}basic/event/${this.eventId}/participants/`);
      this.allGroups = result.data[0].scoutOrganisations;
      this.sliceGroups();
      await this.setCurrent(0);
    },
    sliceGroups() {
      this.allGroups.forEach(((value, index) => {
        const chunkIndex = Math.floor(index / this.groupsPerDocument); // calculates current doc
        if (!this.groupParts[chunkIndex]) {
          this.groupParts[chunkIndex] = []; // starts a new doc
        }
        this.groupParts[chunkIndex].push(value);
      }));
    },
    async setCurrent(index) {
      this.current = this.groupParts[index];
      // Forces DOM update
      await this.$forceUpdate();
      // Waits to ensure correct loading from next document
      return new Promise((resolve) => {
        this.$nextTick(() => {
          setTimeout(() => {
            this.$emit('loadingDone');
            resolve();
          }, 4000);
        });
      });
    },
  },
  created() {
    this.loadData();
  },
};
</script>

<style lang="scss" scoped>
.pdf-content {
  .v-card.v-sheet.bdp-color {
    border: 5px solid yellow !important
  }

  .v-card.v-sheet.dpv-color {
    border: 5px solid blue !important
  }

  .v-card h5  span.will_bleiben {
    border-bottom: 2px solid;
  }

  .v-card h5 span.heim_aber_egal {
    border-bottom: 3px dotted;
  }
}
</style>

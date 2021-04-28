<template>
  <v-container fluid class="pa-0">
    <v-row class="center text-center justify-center pa-0">
      <v-card class="mx-auto pa-0" flat>
        <v-card-text class="pa-0">
          <v-container class="pa-0" fluid>
            <v-row class="pa-0">
              <v-col cols="12" md="6">
                <kpi-card :data="kpiCardOne" color="red lighten-1" />
              </v-col>
              <v-col cols="12" md="6">
                <kpi-card :data="kpiCardTwo" color="blue lighten-1" />
              </v-col>
            </v-row>
            <v-row class="pa-0">
              <v-col cols="12" md="6">
                <kpi-card-list :data="kpiCardThree" color="teal lighten-1" />
              </v-col>
              <v-col cols="12" md="6">
                <kpi-card-list
                  :data="kpiCardFour"
                  color="light-green lighten-1"
                />
              </v-col>
            </v-row>
          </v-container>
        </v-card-text>
      </v-card>
    </v-row>
  </v-container>
</template>

<script>
import { serviceMixin } from '@/mixins/serviceMixin';
import kpiCard from '@/components/kpi/Card.vue';
import kpiCardList from '@/components/kpi/CardList.vue';

export default {
  mixins: [serviceMixin],
  components: {
    kpiCard,
    kpiCardList,
  },
  data: () => ({
    data: [],
  }),
  computed: {
    eventId() {
      return this.$route.params.id;
    },
    confirmedData() {
      return this.data.filter((item) => item.isConfirmed);
    },
    kpiCardOne() {
      return {
        header: 'Anmeldungen',
        subheader: 'Bestätigt',
        dataOne: this.confirmedData.reduce(
          (accum, item) => accum + item.numberParticipant,
          0,
        ),
        dataTwo: this.confirmedData.reduce(
          (accum, item) => accum + item.numberHelper,
          0,
        ),
        dataOneName: 'Teilnehmer',
        dataTwoName: 'Helfer',
      };
    },
    kpiCardTwo() {
      return {
        header: 'Anzahl Stämme',
        subheader: 'aus den Bünden',
        dataOne: this.confirmedData.filter((item) => item.verbandName === 'BdP')
          .length,
        dataTwo: this.confirmedData.filter((item) => item.verbandName === 'DPV')
          .length,
        dataOneName: 'BdP',
        dataTwoName: 'DPV',
      };
    },
    kpiCardThree() {
      return {
        header: 'Letzen Anmeldungen',
        dataOne: this.confirmedData,
        subheader: 'Nach Bestätigundsdatum',
        rankField: 'updatedAt',
        rankOrder: 'desc',
      };
    },
    kpiCardFour() {
      return {
        header: 'Größte Anmeldungen',
        subheader: 'nach Gesamtteilnehmer',
        dataOne: this.confirmedData,
        rankField: 'numberParticipant',
        rankOrder: 'desc',
      };
    },
  },
  methods: {
    getNumberParticipant(item) {
      return `${item.numberParticipant || 0} (${item.numberHelper || 0})`;
    },
    getData(eventId) {
      this.getRegistrationStats(eventId).then((responseObj) => {
        this.data = responseObj.data;
      });
    },
  },
  created() {
    this.getData(this.eventId);
  },
};
</script>

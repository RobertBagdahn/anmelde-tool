<template>
  <v-tabs vertical icons-and-text class="pa-0">
    <v-tab class="pa-0">
      <v-icon left> mdi-table-headers-eye </v-icon>
      KPI
    </v-tab>
    <v-tab>
      <v-icon left> mdi-table </v-icon>
      Tabelle
    </v-tab>

    <v-tab-item>
      <v-card flat>
        <v-card-text>
          <Kpi />
        </v-card-text>
      </v-card>
    </v-tab-item>

    <v-tab-item>
      <v-card flat>
        <v-card-text>
          <List />
        </v-card-text>
      </v-card>
    </v-tab-item>
  </v-tabs>
</template>

<script>
import List from './tabs/List.vue';
import Kpi from './tabs/Kpi.vue';

export default {
  components: {
    List,
    Kpi,
  },
};
</script>

<template>
  <v-app>
    <div id="app">
      <main-comp/>
    </div>
  </v-app>
</template>

<script>
import MainComp from './views/Main.vue';

export default {
  name: 'App',

  components: {
    MainComp,
  },
  created() {
    document.title = 'Anmelde-Tool für Pfadfinder_innen';
  },
  data: () => ({
    //
  }),
};
</script>

<style>
.top-margin {
  margin-top: 70px !important;
}

#app {
  background-color: rgba(240, 236, 236, 0.185);
}
</style>

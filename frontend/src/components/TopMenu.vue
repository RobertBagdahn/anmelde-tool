<template>
  <v-app-bar app color="primary" dark absolute>
    <v-tabs background-color="primary" centered dark icons-and-text>
      <v-tab>
        <router-link to="/">
          <img
            :src="logoPath"
            height="40"
            alt="Logo"
            class="logo-img mx-2"
          />
        </router-link>
      </v-tab>

      <v-spacer></v-spacer>
      <v-tab
        v-if="isAuthenticated"
        @click="$router.push({ name: 'eventOverview' })"
      >
        Fahrten
        <v-icon>mdi-view-list</v-icon>
      </v-tab>
      <v-spacer></v-spacer>
      <v-tab
        v-if="isAuthenticated"
        @click="$router.push({ name: 'settingsUser' })"
      >
        Profil
        <v-icon>mdi-account-circle</v-icon>

      </v-tab>
    </v-tabs>
  </v-app-bar>
</template>

<script>
import { mapGetters } from 'vuex';

export default {
  name: 'TopMenu',

  data: () => ({}),
  computed: {
    ...mapGetters(['isAuthenticated', 'getJwtData']),
    userName() {
      return this.getJwtData.email;
    },
    logoPath() {
      if (process.env.VUE_APP_ENV === 'DEV') {
        return require('../assets/logo_dpv_beta.png'); // eslint-disable-line
      }
      return require('../assets/logo_bdp_dpv.svg'); // eslint-disable-line
    },
    isSimpleUser() {
      if (this.getJwtData) {
        return !(this.getJwtData.groups.length || this.getJwtData.isStaff);
      }
      return true;
    },
    logoutText() {
      if (this.$vuetify.breakpoint.mobile) {
        return '';
      }
      return 'Logout';
    },
  },
  methods: {
    onLogoutClicked() {
      this.$store.commit('clearTokens');
      this.$router.push({ name: 'landing' });
    },
  },
};
</script>

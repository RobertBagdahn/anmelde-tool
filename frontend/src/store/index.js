import Vue from 'vue';
import Vuex from 'vuex';
import VueJwtDecode from 'vue-jwt-decode';
import createPersistedState from 'vuex-persistedstate'; // eslint-disable-line

Vue.use(Vuex);
Vue.use(VueJwtDecode);

export default new Vuex.Store({
  state: {
    accessToken: null,
    refreshToken: null,
    ageGroupMapping: [],
    roleMapping: [],
    scoutOrgaLevelMapping: [],
    participantRoleMapping: [],
    hierarchyMapping: [],
    eatHabitTypeMapping: [],
    travelTypeTypeMapping: [],
    tentTypeMapping: [],
    currentEventParticipants: [],
    dpvAddedLocation: false,
    apiIsDown: false,
  },
  getters: {
    dpvAddedLocation(state) {
      return state.dpvAddedLocation;
    },
    getJwtData(state) {
      return VueJwtDecode.decode(state.accessToken);
    },
    isAuthenticated(state) {
      return !!state.accessToken;
    },
    ageGroupMapping(state) {
      return state.ageGroupMapping;
    },
    currentEventParticipants(state) {
      return state.currentEventParticipants;
    },
    roleMapping(state) {
      return state.roleMapping;
    },
    scoutOrgaLevelMapping(state) {
      return state.scoutOrgaLevelMapping;
    },
    participantRoleMapping(state) {
      return state.participantRoleMapping;
    },
    eatHabitTypeMapping(state) {
      return state.eatHabitTypeMapping;
    },
    travelTypeTypeMapping(state) {
      return state.travelTypeTypeMapping;
    },
    hierarchyMapping(state) {
      return state.hierarchyMapping;
    },
    tentTypeMapping(state) {
      return state.tentTypeMapping;
    },
    apiIsDown(state) {
      return state.apiIsDown;
    },
  },
  mutations: {
    setTokens(state, access, refresh) {
      state.accessToken = access;
      state.refreshToken = refresh;
    },
    clearTokens(state) {
      state.accessToken = null;
      state.refreshToken = null;
    },
    setAgeGroupMapping(state, newAgeGroup) {
      state.ageGroupMapping = newAgeGroup;
    },
    setCurrentEventParticipants(state, newData) {
      state.currentEventParticipants = newData;
    },
    setRoleMapping(state, newData) {
      state.roleMapping = newData;
    },
    setScoutOrgaLevelMapping(state, newData) {
      state.scoutOrgaLevelMapping = newData;
    },
    setParticipantRoleMapping(state, newData) {
      state.participantRoleMapping = newData;
    },
    setEatHabitTypeMapping(state, newData) {
      state.eatHabitTypeMapping = newData;
    },
    setTravelTypeTypeMapping(state, newData) {
      state.travelTypeTypeMapping = newData;
    },
    setHierarchyMapping(state, newData) {
      state.hierarchyMapping = newData;
    },
    setTentTypeMapping(state, newData) {
      state.tentTypeMapping = newData;
    },
    apiIsDown(state, status) {
      state.apiIsDown = status;
    },
  },
  actions: {
  },
  modules: {
  },
  plugins: [createPersistedState()],
});

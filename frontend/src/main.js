import Vue from 'vue';
import Vuelidate from 'vuelidate';
import VueJwtDecode from 'vue-jwt-decode';
import VuetifyMoney from 'vuetify-money';
import VueGoogleCharts from 'vue-google-charts';
import VueLodash from 'vue-lodash';
import lodash from 'lodash';
import AsyncComputed from 'vue-async-computed';
import moment from 'moment';

import App from './App.vue';
import router from './router';
import store from './store';
import vuetify from './plugins/vuetify';
import auth from './auth';

import 'material-design-icons-iconfont/dist/material-design-icons.css';

const VueMoment = require('vue-moment');

Vue.config.productionTip = false;

Vue.use(Vuelidate);
Vue.use(VueJwtDecode);
Vue.use(VuetifyMoney);
Vue.use(VueGoogleCharts);
Vue.use(AsyncComputed);
Vue.use(VueMoment);

Vue.use(VueLodash, { lodash });

auth.interceptorsSetup(store, router);

Vue.prototype.moment = moment;

new Vue({
  router,
  store,
  vuetify,
  render: (h) => h(App),
}).$mount('#app');

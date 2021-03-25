import Vue from 'vue'
import VueRouter from 'vue-router'
import Amplify from 'aws-amplify';
import '@aws-amplify/ui-vue';
import Vuetify from 'vuetify/lib';
import VueCoreVideoPlayer from 'vue-core-video-player';
import DatetimePicker from 'vuetify-datetime-picker';

import aws_exports from './aws-exports';
import App from './App.vue'
import Clips from './components/Clips.vue'
import Events from './components/Events.vue'
import vuetify from './plugins/vuetify';
import http from './plugins/http.js'

Vue.config.productionTip = false;
Vue.use(VueRouter);
Vue.use(Vuetify);
Vue.use(http);
Vue.use(VueCoreVideoPlayer);
Vue.use(DatetimePicker);
Amplify.configure(aws_exports);

const router = new VueRouter({
  mode: 'history',
  base: __dirname,
  routes: [
    {
      path: '/',
      component: Events,
    },
    {
      path: '/event/:id',
      component: Clips,
    }
  ]
})

new Vue({
  router,
  vuetify,
  render: h => h(App)
}).$mount('#app')

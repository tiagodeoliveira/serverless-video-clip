<template>
    <v-simple-table>
        <thead>
            <tr>
              <th class="text-center" colspan="2">
                <a :href="'event/' + item.id">
                  <h3>{{item.name}} - {{item.description}}</h3>
                </a>
                </th>
            </tr>
        </thead>            
        <tbody>
            <tr>
                <td>ID</td>
                <td><v-icon color="primary" dark>mdi-barcode</v-icon>{{item.id}}
            </td>
            </tr>
            <tr>
                <td>State</td>
                <td><v-icon :color="getStateColor(item.state)" dark >{{getStateIcon(item.state)}}</v-icon>{{ item.state }}</td>
            </tr>
            <tr>
                <td>Begin</td>
                <td><v-icon color="primary" dark>mdi-calendar-clock</v-icon>{{ getStartTime }}</td>
            </tr>
            <tr>
                <td>End</td>
                <td><v-icon color="primary" dark>mdi-calendar-clock</v-icon>{{ getEndTime }}</td>
            </tr>
            <tr v-if="['creating', 'created', 'running', 'starting'].includes(item.state)">
                <td>Rtmp Endpoints</td>
                <td>
                    <ul>
                        <li v-for="(e, i) in getEndpointsList(item.endpoints)" :key="i">{{e}}</li>
                    </ul>
                </td>
            </tr>
            <tr v-if="item.state === 'running'">
                <td>Livestream</td>
                <td>
                  <div class="player-container">
                    <vue-core-video-player autoplay :core="HLSCore" :src="item.stream_url" style="width: 500px;"></vue-core-video-player>
                  </div>                  
                </td>
            </tr>
        </tbody>
    </v-simple-table>
</template>
<script>
import HLSCore from '@core-player/playcore-hls';
import * as formatUtils from '../utils/format.js';

export default {
  name: 'Event',
  props: {
      item: Object
  },
  async created() {
		this.interval = setInterval(() => this.$forceUpdate(), 1000);
  },  
  computed: {
    getStartTime() {
      return formatUtils.formatTime(this.item.start);
    },
    getEndTime() {
      return formatUtils.formatTime(this. item.end)
    }
  },
  data: () => ({
    HLSCore,
    interval: null,
  }),
  methods: {
    formatTime: formatUtils.formatTime, 
    getStateIcon: formatUtils.getStateIcon, 
    getStateColor: formatUtils.getStateColor,
    getEndpointsList(e) {
      const items = e.replace(']', '').replace('[', '').replaceAll("'", '').split(',').map(i => i.trim());
      return items;
    },          
  }
};
</script>

<style scoped>
table {
    padding-bottom: 15px;
}
th {
    background-color: beige;
}
</style>
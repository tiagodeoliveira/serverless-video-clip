<template>
  <v-simple-table>
        <thead>
            <tr>
                <th class="text-center" colspan="2">
                    <h3>{{item.name}} - {{item.description}}</h3>
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
                <td><v-icon color="primary" dark>mdi-calendar-clock</v-icon>{{ formatTime(item.start) }}</td>
            </tr>
            <tr>
                <td>End</td>
                <td><v-icon color="primary" dark>mdi-calendar-clock</v-icon>{{ formatTime(item.end) }}</td>
            </tr>
            <tr v-if="item.state === 'published'">
                <td>Votes</td>
                <td><v-icon color="primary" dark>mdi-thumb-up</v-icon>{{votesUp}} - <v-icon color="primary" dark>mdi-thumb-down</v-icon>{{votesDown}}</td>
            </tr>
            <tr v-if="item.state === 'published'">
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
import * as formatUtils from '../utils/format.js';
import HLSCore from '@core-player/playcore-hls';
import { API, graphqlOperation } from 'aws-amplify';
import { listVotes } from '../graphql/queries';
import { onCreateVote } from '../graphql/subscriptions';

export default {
    name: 'Clip',
    props: {
      item: Object
    },
    data: () => ({
        HLSCore,
        votesUp: 0,
        votesDown: 0,
    }),   
    async created() {
        this.getVotes();
        this.subscribe();
    },       
    methods: {
        formatTime: formatUtils.formatTime, 
        getStateIcon: formatUtils.getStateIcon, 
        getStateColor: formatUtils.getStateColor,     
        async getVotes() {
            const votesData = await API.graphql(
                graphqlOperation(listVotes, {
                    filter: {
                        "clip_id": this.item.id
                    }
                })
            );
            const votes = votesData.data.listVotes.items
            this.votesUp = votes.filter(v => v.vote === "up").length;
            this.votesDown = votes.filter(v => v.vote === "down").length;
        },
        async subscribe() {
            API.graphql(graphqlOperation(onCreateVote, { filter: { 'clip_id': this.item.id }})).subscribe({
                next: (eventData) => {
                    const vote = eventData.value.data.onCreateVote;
                    if (vote.vote === "down") {
                        this.votesDown += 1;
                    } else {
                        this.votesUp += 1;
                    }
                }
            });            
        }
    },
}
</script>

<style scoped>
table {
    padding-bottom: 15px;
}
th {
    background-color: beige;
}
</style>
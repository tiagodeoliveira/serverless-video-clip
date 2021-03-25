<template>
  <v-row align="center">
    <v-card class="mx-auto" tile>
        <v-card-title>Clips</v-card-title>
        <v-card-subtitle>{{eventId}}</v-card-subtitle>
        <v-simple-table>
          <tbody>
              <tr v-for="item in clips" :key="item.id">
                <clip v-bind:item="item" />                
              </tr>
          </tbody>
        </v-simple-table>        
        <v-card-actions>
          <v-btn color="primary" @click="dialog = !dialog">
            <v-icon>mdi-plus</v-icon>
          </v-btn>
        </v-card-actions>        

    <v-dialog v-model="dialog" max-width="800px">
      <v-card>
        <v-card-title class="headline">Create new Clip</v-card-title>
          <v-container>
            <v-form ref="newClipForm" v-model="valid">
              <v-text-field
                v-model="newClip.name"
                label="Clip Name"
                required
              ></v-text-field>
              <v-text-field
                v-model="newClip.description"
                label="Clip Description"
                required
              ></v-text-field>

              <v-row>
                <v-col cols="6" sm="6" md="6">
                  <v-datetime-picker label="Clip Start" v-model="newClip.start" @input="updateClipEnd" time-format="HH:mm:ss"></v-datetime-picker>
                </v-col>
                <v-col cols="6" sm="6" md="6">
                  <v-datetime-picker label="Clip End" v-model="newClip.end" time-format="HH:mm:ss"></v-datetime-picker>
                </v-col>                
              </v-row>

              <v-btn :disabled="sending" class="mr-4" color="primary" @click="createNewClip">submit</v-btn>
              <v-progress-linear 
                :active="sending"
                height="10"
                color="primary"
                indeterminate
              ></v-progress-linear>
            </v-form>   
          </v-container>
      </v-card>
    </v-dialog>    
    </v-card>
  </v-row>
</template>

<script>
import moment from 'moment';
import { API, graphqlOperation } from 'aws-amplify';
import { listClips } from '../graphql/queries';
import { onCreateClip, onUpdateClip, onDeleteClip } from '../graphql/subscriptions';
import Clip from './Clip';

export default {
  name: 'Clips',
  components: {
    Clip,
  },  
  data() {
    return {
      clips: [],
      eventId: null,
      dialog: false,
      sending: false,
      valid: false, 
      newClip: {
        name: '',
        description: '',
        start: moment().subtract(7, 'minutes').toDate(),
        end: moment().subtract(5, 'minutes').toDate(),
      }
    }
  },
  async created() {
    this.eventId = this.$route.params.id;
    this.getClips();
    this.subscribe();
  },  
  methods: {
    updateClipEnd(e) {
      this.newClip.end = moment(e).add(10, 'minutes').toDate();
    },
    async createNewClip() {
      this.sending = true;

      const payload = {
        "name": this.newClip.name,
        "description": this.newClip.description,
        "start": moment(this.newClip.start).utcOffset(0).toISOString(),
        "end": moment(this.newClip.end).utcOffset(0).toISOString(),
      };
      console.log(payload);
      this.$http.post(`/transmission/${this.eventId}/clip`, payload)
        .then((response) => {
          console.log(response);
          this.dialog = false;
          this.newClip.name = '';
          this.newClip.description = '';
        })
        .catch((error) => {
          console.log("Network request error", error);
        })
        .finally(() => {
          this.sending = false;
        })
    },
    async getClips() {
      const clips = await API.graphql(
        graphqlOperation(listClips, {
          filter: {
            "event_id": this.eventId 
          }
        })
      );
      this.clips = clips.data.listClips.items;
    },
    async subscribe() {
      API.graphql(graphqlOperation(onDeleteClip, { filter: { 'event_id': this.eventId }})).subscribe({
        next: (eventData) => {
          const clip = eventData.value.data.onDeleteClip;
          console.log('Removing clip', clip);
          const removeIndex = this.clips.map(item => item.id).indexOf(clip.id);
          this.clips.splice(removeIndex, 1);
        }
      });
      API.graphql(graphqlOperation(onUpdateClip, { filter: { 'event_id': this.eventId }})).subscribe({
        next: (eventData) => {
          const clip = eventData.value.data.onUpdateClip;
          console.log('Updating clip', clip);

          const updateIndex = this.clips.map(item => item.id).indexOf(clip.id);
          this.clips[updateIndex].name = clip.name;
          this.clips[updateIndex].description = clip.description;
          this.clips[updateIndex].state = clip.state;
          this.clips[updateIndex].start = clip.start;
          this.clips[updateIndex].end = clip.end;
          this.clips[updateIndex].stream_url = clip.stream_url;
        }
      });
      API.graphql(graphqlOperation(onCreateClip, { filter: { 'event_id': this.eventId }})).subscribe({
        next: (eventData) => {
          const clip = eventData.value.data.onCreateClip;
          console.log('Creating new clip', clip);
          if (this.clips.some(item => item.id === clip.id)) return;
          this.clips.unshift(clip);
        }
      });      
    }
  }
}
</script>

<style scoped>
h3 {
  margin: 40px 0 0;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
</style>

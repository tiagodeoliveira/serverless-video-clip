<template>
  <v-row align="center">
    <v-card class="mx-auto" tile>
        <v-card-title>Events</v-card-title>
        <v-card-text>
          <v-simple-table>
            <tbody>
                <tr v-for="item in transmissions" :key="item.id">
                  <event v-bind:item="item" />                
                </tr>
            </tbody>
          </v-simple-table>
        </v-card-text>

        <v-card-actions>
          <v-btn color="primary" @click="dialog = !dialog">
            <v-icon>mdi-plus</v-icon>
          </v-btn>
        </v-card-actions>        
    </v-card>
    <v-dialog v-model="dialog" max-width="800px">
      <v-card>
        <v-card-title class="headline">Create new event</v-card-title>
          <v-container>
            <v-form ref="newEventForm" v-model="valid">
              <v-text-field
                v-model="newEvent.eventName"
                label="Event Name"
                required
              ></v-text-field>
              <v-text-field
                v-model="newEvent.eventDescription"
                label="Event Description"
                required
              ></v-text-field>
              <v-text-field
                v-model="newEvent.eventProducerCidrs"
                label="Producer CIDRs"
                required
              ></v-text-field>
              <v-row>
                <v-col cols="6" sm="6" md="4">
                  <v-datetime-picker label="Clip Start" v-model="newEvent.eventBegin" @input="updateEventEnd"> </v-datetime-picker>               
                </v-col>
                <v-col cols="6" sm="6" md="4">
                  <v-datetime-picker label="Clip End" v-model="newEvent.eventEnd"> </v-datetime-picker>
                </v-col>                
              </v-row>
              <v-btn :disabled="sending" class="mr-4" color="primary" @click="createNewEvent">submit</v-btn>
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
  </v-row>  
</template>

<script>
import moment from 'moment';
import { API } from 'aws-amplify';
import { listTransmissions } from '../graphql/queries';
import { onCreateTransmission, onUpdateTransmission, onDeleteTransmission } from '../graphql/subscriptions';
import Event from './Event';

function getUTCZeroDate(dateString) {
  const d = new Date(dateString);
  return d.toISOString().substr(0, 19);
}

export default {
  name: 'Events',
  components: {
    Event,
  },
  async created() {
    this.getTransmissions();
    this.subscribe();
  },
  data() {
    return {
      transmissions: [],
      dialog: false,
      valid: false,
      dateMenu: false,
      beginTimeMenu: false,
      endTimeMenu: false,
      sending: false,
      newEvent: {
        eventName: '',
        eventDescription: '',
        eventProducerCidrs: '0.0.0.0/0',
        eventBegin: moment().add(5, 'minutes').toDate(),
        eventEnd: moment().add(10, 'minutes').toDate(),
      },
    }
  },
  computed: {
  },
  methods: {
    updateEventEnd(e) {
      this.newEvent.eventEnd = moment(e).add(10, 'minutes').toDate();
    },    
    async getTransmissions() {
      const transmissions = await API.graphql({
        query: listTransmissions
      });
      this.transmissions = transmissions.data.listTransmissions.items.sort((a, b) => {
        if (b.state === "running") {
          return 0;
        }

        return b.start.localeCompare(a.start);
      });
    },
    async createNewEvent() {
      if (!this.valid) {
        return false;
      }

      this.sending = true
      const startDate = getUTCZeroDate(this.newEvent.eventBegin);
      const endDate = getUTCZeroDate(this.newEvent.eventEnd);
      const producerCidrs = this.newEvent.eventProducerCidrs.trim().split(',').map(c => c.trim());

      const payload = {
        "name": this.newEvent.eventName,
        "description": this.newEvent.eventDescription,
        "start": startDate,
        "end": endDate,
        "producer_cidrs": producerCidrs
      };
      console.log(payload);

      this.$http.post('/transmission', payload)
        .then((response) => {
          console.log(response);
          this.dialog = false;
          this.newEvent.eventName = '';
          this.newEvent.eventDescription = '';
        })
        .catch(function (error) {
          console.log("Network request error", error);
        })
        .finally(() => {
          this.sending = false;
        })
    },
    subscribe() {
      API.graphql({ query: onDeleteTransmission }).subscribe({
        next: (eventData) => {
          const transmission = eventData.value.data.onDeleteTransmission;
          console.log('Removing transmissions', transmission);
          const removeIndex = this.transmissions.map(item => item.id).indexOf(transmission.id);
          this.transmissions.splice(removeIndex, 1);
        }
      });
      API.graphql({ query: onUpdateTransmission }).subscribe({
        next: (eventData) => {
          const transmission = eventData.value.data.onUpdateTransmission;
          console.log('Updating transmission', transmission);

          const updateIndex = this.transmissions.map(item => item.id).indexOf(transmission.id);
          this.transmissions[updateIndex].name = transmission.name;
          this.transmissions[updateIndex].description = transmission.description;
          this.transmissions[updateIndex].state = transmission.state;
          this.transmissions[updateIndex].start = transmission.start;
          this.transmissions[updateIndex].end = transmission.end;
          this.transmissions[updateIndex].endpoints = transmission.endpoints;
        }
      });
      API.graphql({ query: onCreateTransmission }).subscribe({
        next: (eventData) => {
          const transmission = eventData.value.data.onCreateTransmission;
          console.log('Creating new transmission', transmission);
          if (this.transmissions.some(item => item.id === transmission.id)) return;
          this.transmissions.unshift(transmission);
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
v-simple-table {
  padding-bottom: 40px;
  padding-left: 60px;
}
</style>

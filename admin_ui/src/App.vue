<template>
  <v-app>
    <v-app-bar
      app
      color="primary"
      dark
    >
      <a href="/"> 
        <div class="d-flex align-center">
          <v-img
            class="shrink mr-2"
            contain
            :src="require('./assets/logo.png')"
            transition="scale-transition"
            width="40"
          />
          <h3>Event Management</h3>
        </div>
      </a>      

      <v-spacer></v-spacer>
    </v-app-bar>

    <v-main>
      <router-view class="view"></router-view>    
    </v-main>
  </v-app>
</template>

<script>

export default {
  name: 'App',

  data: () => ({
  }),
};
</script>

<style scoped>
h3 {
  color: aliceblue;
}
</style>
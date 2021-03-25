import { StatusBar } from 'expo-status-bar';
import React from 'react';
import { StyleSheet, Text, Button } from 'react-native';
import {Amplify, Auth} from 'aws-amplify'
import config from './aws-exports';
import { Router, Scene } from 'react-native-router-flux';
import Clips from './src/components/Clips';
import Events from './src/components/Events';
import { withAuthenticator } from 'aws-amplify-react-native'

Amplify.configure({
  config
});

const renderDrawerContent = () => {
  return (
    <Text>jsbdfjakbsdfals</Text>
  )
}

const App = () => {
  return (
    <>
      <StatusBar style="light" />
      <Router>
        <Scene key = "root">
          <Scene key = "events" component = {Events} title = "Events" initial = {true} />
          <Scene key = "clips" component = {Clips} title = "Clips" />
        </Scene>
      </Router>
      {/* <Button title="Logout" onPress={() => Auth.signOut({ global: true })}></Button> */}
    </>
  );
}

global.Buffer = require('buffer').Buffer;
export default withAuthenticator(App);

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
    alignItems: 'center',
    justifyContent: 'center',
  },
});

import React, { useState, useEffect } from 'react'
import { Actions } from 'react-native-router-flux';
import { SafeAreaView, View, FlatList, StyleSheet, StatusBar, Text, TouchableOpacity  } from 'react-native';
import { API, graphqlOperation } from 'aws-amplify';
import { listTransmissions } from '../graphql/queries';
import { onUpdateTransmission, onDeleteTransmission } from '../graphql/subscriptions';

const VALID_STATES = ['running', 'finished', 'deleting'];

const Events = () => {
    const [events, setEvents] = useState([]);

    useEffect(() => {
        const updateTransmission = async (transmission) => {
            setEvents(previous => {
                console.log(previous);
                if (previous.filter(i => i.id === transmission.id).length === 0) {
                    return [...previous, transmission];
                }
                return previous;
            })
        }
    
        const removeTransmission = async (transmission) => {
            setEvents(previous => previous.filter(e => e.id !== transmission.id));
        }

        const fetchEvents = async () => {
            const transmissionsData = await API.graphql(graphqlOperation(listTransmissions));
            const eventsData = transmissionsData.data.listTransmissions.items
            const validEvents = eventsData.filter(e => VALID_STATES.includes(e.state));
            setEvents(validEvents);
        }

        fetchEvents();    

        const updateSubs = API.graphql(graphqlOperation(onUpdateTransmission))
            .subscribe({
                next: (eventData) => {
                    const transmission = eventData.value.data.onUpdateTransmission;
                    if (VALID_STATES.includes(transmission.state)) {
                        updateTransmission(transmission);
                    }
                },
                error: error => {
                    // console.warn('Error');
                }            
            });
        const deleteSubs = API.graphql(graphqlOperation(onDeleteTransmission))
            .subscribe({
                next: (eventData) => {
                    console.log('Deleting transmission');
                    const transmission = eventData.value.data.onDeleteTransmission;
                    removeTransmission(transmission);
                },
                error: error => {
                    console.warn('Error');
                }            
            });       

        return () => {
            updateSubs.unsubscribe();
            deleteSubs.unsubscribe();
        }
    }, []);

    const onPress = (id) => {
        Actions.clips({id});
    }

    const renderItem = ({ item }) => (
        <TouchableOpacity onPress={() => onPress(item.id)} style={[styles.item]}>
            <View style={styles.item}>
                <Text style={styles.title}>{item.name}</Text>
                <Text style={styles.title}>{item.description}</Text>
            </View>
        </TouchableOpacity>
    );

    return (
        <SafeAreaView style={styles.container}>
            <FlatList
                data={events}
                renderItem={renderItem}
                keyExtractor={item => item.id}
            />
      </SafeAreaView>        
   )
}

const styles = StyleSheet.create({
    container: {
      flex: 1,
      marginTop: StatusBar.currentHeight || 0,
    },
    item: {
      backgroundColor: '#D2EDC4',
      padding: 20,
      marginVertical: 8,
      marginHorizontal: 16,
    },
    title: {
      fontSize: 20,
    },
    subTitle: {
        fontSize: 10,
    }
  });

export default Events
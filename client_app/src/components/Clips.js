import React, { useState, useEffect } from 'react'
import { SafeAreaView, View, FlatList, StyleSheet, StatusBar, Text, TouchableOpacity  } from 'react-native';
import { API, graphqlOperation } from 'aws-amplify';
import Video from 'react-native-video'; 
import { Ionicons } from '@expo/vector-icons';
import { listVotes, listClips } from '../graphql/queries';
import { createVote } from '../graphql/mutations';
import { onUpdateClip, onDeleteClip } from '../graphql/subscriptions';

const fetchVotes = async (clipId, setVotes) => {
    try {
        const clipsData = await API.graphql(graphqlOperation(listVotes, { filter: { "clip_id": clipId } }));
        const votes = clipsData.data.listVotes.items
        const votesUp = votes.filter(v => v.vote === "up").length;
        const votesDown = votes.filter(v => v.vote === "down").length;
        setVotes({up: votesUp, down: votesDown});
      } catch (err) { 
          console.error('error fetching events', err);
    }    
}

const saveVote = async (vote, clipId, setVotes) => {
    try {
        await API.graphql(graphqlOperation(createVote, { 
            clip_id: clipId,
            vote: vote,
            user_id: 'user'
        })); 
        fetchVotes(clipId, setVotes);
    } catch (e) {
        console.log ("failed", e);
    }
}

const Clips = (props) => {

    let video;
    const [clips, setClips] = useState([]);
    const [selectedClip, setSelectedClip] = useState(false);
    const [paused, setPaused] = useState(false);
    const [votes, setVotes] = useState({});

    const fetchClips = async () => {
        console.log('Fetching clips');
        const clipsData = await API.graphql(graphqlOperation(listClips, { filter: { "event_id": props.id } }));
        const foundClips = clipsData.data.listClips.items;
        setClips(foundClips.filter(c => c.state === 'published'));
    }

    const subscribeClips = async() => {
        API.graphql(graphqlOperation(onUpdateClip, { filter: { "event_id": props.id } }))
        .subscribe({
            next: (eventData) => {
                const clip = eventData.value.data.onUpdateClip;
                console.log('new clip', clip);
                if (clip.state === 'published') {
                    setClips(previous => {
                        if (previous.filter(i => i.id === clip.id).length === 0) {
                            return [...previous, clip];
                        }

                        return previous;
                    })
                }
            },
            error: error => {
                // console.warn('Error');
            }            
        });   
        API.graphql(graphqlOperation(onDeleteClip, { filter: { "event_id": props.id } }))
            .subscribe({
                next: (eventData) => {
                    const clipData = eventData.value.data.onDeleteClip;
                    setClips(previous => previous.filter(c => c.id !== clipData.id));
                },
                error: error => {
                    // console.warn('Error');
                }            
            });          
    }      

    useEffect(() => {
        fetchClips();
        subscribeClips();
    }, []);

    const selectClip = async (clip) => {
        setSelectedClip(clip);
        fetchVotes(clip.id, setVotes);
    };

    const renderVideoPlayer = () => {
        if (selectedClip) {
            return (
                <View style={styles.fullScreen}>
                    <TouchableOpacity style={styles.fullScreen} onPress={() => setPaused(!paused)}>
                    <Video
                        source={{uri: selectedClip.stream_url}} 
                        style={styles.fullScreen}
                        paused={paused}
                        repeat={false}
                    />
                    </TouchableOpacity>

                    <View style={styles.controls}>
                        <View style={styles.generalControls}>
                            <View style={styles.rateControl}>
                                <TouchableOpacity style={styles.vottingUp} onPress={() => saveVote("up", selectedClip.id, setVotes)}>                                   
                                    <Text>{votes.up} <Ionicons name="md-thumbs-up" size={32} color="green" /></Text>
                                </TouchableOpacity>
                                
                                <TouchableOpacity style={styles.vottingDown} onPress={() => saveVote("down", selectedClip.id, setVotes)}>
                                    <Text><Ionicons name="md-thumbs-down" size={32} color="red" /> {votes.down}</Text>
                                </TouchableOpacity>
                            </View>
                        </View>                        
                    </View>
                </View>
            )
        }
    }

    const renderItem = ({ item }) => (
        <TouchableOpacity onPress={() => selectClip(item)} style={[styles.item]}>
            <View style={styles.item}>
                <Text style={styles.title}>{item.name}</Text>
                <Text style={styles.title}>{item.description}</Text>
            </View>       
        </TouchableOpacity>
    );

    return (
        <SafeAreaView style={styles.container}>
            <FlatList
                data={clips}
                renderItem={renderItem}
                keyExtractor={item => item.id}
            />
            {renderVideoPlayer()}
        </SafeAreaView>        
    )
}

const styles = StyleSheet.create({
    vottingUp: {
        paddingRight: 10,
    },
    vottingDown: {
        paddingLeft: 10,
    },
    container: {
        flex: 1,
        marginTop: StatusBar.currentHeight || 0,
    },  
    fullScreen: {
        position: 'absolute',
        top: 0,
        left: 0,
        bottom: 0,
        right: 0,
      },  
      controls: {
        backgroundColor: 'transparent',
        borderRadius: 5,
        position: 'absolute',
        bottom: 20,
        left: 20,
        right: 20,
      },
      generalControls: {
        flex: 1,
        flexDirection: 'row',
        borderRadius: 4,
        overflow: 'hidden',
        paddingBottom: 10,
      },       
      rateControl: {
        flex: 1,
        flexDirection: 'row',
        justifyContent: 'center',
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


export default Clips
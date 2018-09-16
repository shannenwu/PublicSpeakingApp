import React, { Component } from 'react';
import { View, Text, StyleSheet, TouchableOpacity } from 'react-native';
import { Camera, Permissions } from 'expo';

export default class RecordingScreen extends Component {
    constructor(props){
        super(props);
        this.state = {
            hasCameraPermission: null,
            hasAudioPermission: null
        };
    }
    
    async componentWillMount() {
        const { camera_status } = await Permissions.askAsync(Permissions.CAMERA);
        const { audio_status } = await Permissions.askAsync(Permissions.AUDIO_RECORDING);
        this.setState({
            hasCameraPermission: camera_status === 'granted',
            hasAudioPermission: audio_status === 'granted',
        });
    }

    // record = async () => {
    //     if (this.camera)
    // }
    
    render() {
        const { hasCameraPermission, hasAudioPermission } = this.state;
        const { navigate } = this.props.navigation;
        const styles = StyleSheet.create({
            container: {
                flex: 1,
                backgroundColor: '#78a6f2'
            },
            text: {
                fontFamily: 'latoBold',
                color: 'white',
            }
        });

        if (hasCameraPermission === null || hasAudioPermission === null) {
            return <View style={styles.container} />;
        } else if (hasCameraPermission === false || hasAudioPermission === false) {
            navigate('Start');
            return <View style={styles.container} />;
        } else {
            return(
                <View style={styles.container}>
                    <Camera
                        style={{ flex: 1 }}
                        type={Camera.Constants.Type.front}
                        ref={ref => { this.camera = ref; }}
                    >
                    </Camera>
                </View>
            );
        }
    }
}
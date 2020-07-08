import React, { Component } from 'react';
import {
    StyleSheet,
    Text,
    TouchableOpacity,
    View,
    Image,
    Button,
} from 'react-native';

import * as ImagePicker from 'expo-image-picker';
import * as Permissions from 'expo-permissions';

export default class ImagePickerComponent extends Component {
    constructor(props) {
        super(props);
        this.state = {image: null};
        // this.state = {
        //     image: require('../assets/icon.png'),
        //     localImage: 1
        // };
    }

    takePicture = async() => {
        await Permissions.askAsync(Permissions.CAMERA);
        const {cancelled, uri} = await ImagePicker.launchCameraAsync({
            allowsEditing: true,
            aspect: [1,1],
            quality: 0.5
        });
        if (!cancelled) this.setState({image: uri});
    };

    // checkLocalImageStatus() {
    //     if (this.state.localImage == 1) {
    //         <Image style={{width: 100, height: 100}} source={this.state.image}/>
    //     } else {
    //         <Image style={{width: 100, height: 100}} source={{uri: this.state.image}} />
    //     }
    // }

    render() {
        //return a image as a button
        return (
            <View
                style={styles.container}>
                <TouchableOpacity
                    activityOpacity={0.5}
                    style={styles.container}
                    onPress={this.takePicture.bind(this)}>
                    {/*{this.checkLocalImageStatus()}*/}
                    {this.state.image && <Image style={{width: 100, height: 100}} source={{uri: this.state.image}} /> }
                    {/* <Image style={{width: 100, height: 100}} source={this.state.image} />*/}
                </TouchableOpacity>
            </View>
        );
    }
}

const styles = StyleSheet.create({
    container: {
        height: 100,
        width: 100,
        backgroundColor: 'lightgrey',
        alignItems: 'center',
        justifyContent: 'center'},
});

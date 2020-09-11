import * as React from 'react';
import {Button, Image, View, Platform, TouchableOpacity, Text} from 'react-native';
import * as ImagePicker from 'expo-image-picker';
import * as Permissions from 'expo-permissions';
import axios from "axios";
import styles from "../config/styles";
export default class OcrScanner2 extends React.Component {
    state = {
        image: null,
    };
    scanPicture = (uri) => {
        let reqData = new FormData();
        reqData.append("isOverlayRequired","false");
        reqData.append("filetype","JPG");
        reqData.append("url", {
            uri: uri,
            type: "image/jpeg",
            name: "file"
        });
        axios.post('https://api.ocr.space/Parse/Image', reqData,{
            headers:{
                'Content-Type': 'multipart/form-data',
                'apikey' : 'f748e6bec288957'
            }
        })
            .then(res => {
                if(res.status === 200) {
                    let text = res.data.ParsedResults[0].ParsedText
                    var lines = text.split('\n')
                    let found = false
                    lines.forEach(line => {
                        if(line.startsWith('ISBN')){
                            let isbn = line.split(' ')[1].replace(/(\r\n|\n|\r)/gm, "").replace(/-/g,"")
                            this.props.navigation.navigate('BookCataloguing', {isbn: isbn.toString()})
                            found = true
                        }
                    })
                    if(!found) {
                        alert("No ISBN found in the image")
                        console.log('No ISBN found in the image')
                    }
                }else{
                    alert("Failed to scan the image")
                    console.log('Failed to scan the image')
                }
            }).catch((error)=>{
            console.log(error.message);
        });
    }
    takePicture = async() => {
        await Permissions.askAsync(Permissions.CAMERA);
        const {cancelled, uri} = await ImagePicker.launchCameraAsync({
            allowsEditing: true,
            aspect: [4,3],
            quality: 1
        });
        if (!cancelled) {
            this.setState({image: uri});
            this.scanPicture(uri)
        }
    };

    render() {

        return (
            <View style={{flex:1}}>
                <View style={styles.ocrView}>
                    <View style={styles.noteView}>
                        <Text style={styles.noteText}>
                        Note: Please take a clear picture</Text>
                        <Text style={styles.bulletText}>
                            To make sure your context includes only one line "ISBN + 10 or 13 isbn-digits", you can:</Text>
                        <Text style={styles.bulletText}>1. iOS phone: zoom in the image </Text>
                        <Text style={styles.bulletText}>2. Android phone: crop the image</Text>
                    </View>
                    <Button title="Pick an image from camera roll" onPress={this._pickImage} />
                    <Button title="Go to Camera" onPress={this.takePicture.bind(this)} />
                </View>
                <TouchableOpacity
                    style={styles.manualCloseButton}
                    onPress={() => {this.props.navigation.navigate("Active Listing",{refresh:true})}}>
                    <Text style={{ fontSize: 20, color: 'black'}}> x </Text>
                </TouchableOpacity>
            </View>
        );
    }

    componentDidMount() {
        this.getPermissionAsync();
    }

    getPermissionAsync = async () => {
        if (Platform.OS !== 'web') {
            const { status } = await Permissions.askAsync(Permissions.CAMERA_ROLL);
            if (status !== 'granted') {
                alert('Sorry, we need camera roll permissions to make this work!');
            }
        }
    };

    _pickImage = async () => {
        try {
            let result = await ImagePicker.launchImageLibraryAsync({
                allowsEditing: true,
                aspect: [4, 3],
                quality: 1,
            });
            if (!result.cancelled) {
                this.setState({ image: result.uri });
                this.scanPicture(result.uri)
            }

            console.log(result);
        } catch (E) {
            console.log(E);
        }
    };
}

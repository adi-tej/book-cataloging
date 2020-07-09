import React, {  Component } from 'react';
import {
    Text,
    View,
    TextInput,
    Alert,
    TouchableOpacity,
    ScrollView,
} from 'react-native';

import * as Permissions from "expo-permissions";
import * as ImagePicker from "expo-image-picker";
import ShowCarousel from "./ShowCarousel";
import styles from "../config/styles";


export default class Listing extends Component{
    constructor(props) {
        super(props);
        this.imageID = 0;
        this.state = {
            Title:"",
            ISBN: "",
            Genre: "",
            Author: "",
            Pages: 0,
            Publisher:"",
            Price: 0,
            Other_details: "",
            imageArray:[],
            initImage: null,
        }
    }

    onButtonPress() {
        Alert.alert("Listing book: " + this.state.Title)
    }

    deleteImage = (index) =>{
        const copyImageArray = Object.assign([], this.state.imageArray);
        copyImageArray.splice(index, 1)
        this.setState({
            imageArray: copyImageArray
        })
    };

    takePicture = async() => {
        await Permissions.askAsync(Permissions.CAMERA);
        const {cancelled, uri} = await ImagePicker.launchCameraAsync({
            allowsEditing: true,
            aspect: [1,1],
            quality: 0.5
        });
        if (!cancelled) {
            this.setState({initImage: uri});
            //add this image to imageArray
            this.imageID = this.imageID + 1;
            const copyImageArray = Object.assign([], this.state.imageArray);
            copyImageArray.push({
                id: this.imageID,
                image: this.state.initImage
            })
            this.setState({
                imageArray: copyImageArray
            })
        }
    };

    render() {
        return (
            <View style={styles.container}>
                <View>
                    <ScrollView horizontal={true} style={{flexDirection: "row"}}>
                        {
                            this.state.imageArray.map((image, index)=>{
                                return(
                                    <ShowCarousel
                                        image={image.image}
                                        key={image.id}
                                        delete={this.deleteImage.bind(this, index)}
                                    />
                                )
                            })
                        }
                        <TouchableOpacity
                            activityOpacity={0.5}
                            style={styles.imageContainer}
                            onPress={this.takePicture.bind(this)}>
                            <Text style={styles.loginText}>+</Text>
                        </TouchableOpacity>
                    </ScrollView>
                </View>
                <ScrollView>
                    <Text style={styles.listingTitle}>Title: </Text>
                    <TextInput
                        underlineColorAndroid={"transparent"}
                        style={styles.textInput}
                        onChangeText={(Title) => this.setState({Title})}
                    />

                    <Text style={styles.listingTitle}>ISBN: </Text>
                    <TextInput
                        underlineColorAndroid={"transparent"}
                        style={styles.textInput}
                        keyboardType="number-pad"
                        onChangeText={(ISBN) => this.setState({ISBN})}
                    />

                    <Text style={styles.listingTitle}>Genre: </Text>
                    <TextInput
                        underlineColorAndroid={"transparent"}
                        style={styles.textInput}
                        onChangeText={(Genre) => this.setState({Genre})}
                    />

                    <Text style={styles.listingTitle}>Author: </Text>
                    <TextInput
                        underlineColorAndroid={"transparent"}
                        style={styles.textInput}
                        onChangeText={(Author) => this.setState({Author})}
                    />

                    <Text style={styles.listingTitle}>Page: </Text>
                    <TextInput
                        underlineColorAndroid={"transparent"}
                        style={styles.textInput}
                        onChangeText={(Page) => this.setState({Page})}
                    />

                    <Text style={styles.listingTitle}>Publisher: </Text>
                    <TextInput
                        underlineColorAndroid={"transparent"}
                        style={styles.textInput}
                        onChangeText={(Publisher) => this.setState({Publisher})}
                    />

                    <Text style={styles.listingTitle}>Price: </Text>
                    <TextInput
                        underlineColorAndroid={"transparent"}
                        style={styles.textInput}
                        onChangeText={(Price) => this.setState({Price})}
                    />

                    <Text style={styles.listingTitle}>Other Details: </Text>
                    <TextInput
                        underlineColorAndroid={"transparent"}
                        style={styles.textInput}
                        onChangeText={(Other_details) => this.setState({Other_details})}
                    />
                </ScrollView>

                <TouchableOpacity
                    activityOpacity={0.5}
                    style={styles.loginButton}
                    onPress={this.onButtonPress.bind(this)}>
                    <Text style={styles.loginText}>List on eBay</Text>
                </TouchableOpacity>
            </View>
        )
    }
}

import React, {  Component } from 'react';
import {
    Text,
    View,
    TextInput,
    Alert,
    TouchableOpacity,
    ScrollView,
    StyleSheet,
    SafeAreaView,
} from 'react-native';
import { KeyboardAwareScrollView } from 'react-native-keyboard-aware-scroll-view'
import RNPickerSelect from "react-native-picker-select";
import {Icon} from "native-base";

import * as Permissions from "expo-permissions";
import * as ImagePicker from "expo-image-picker";

import ShowCarousel from "./ShowCarousel";
import styles from "../config/styles";


export default class BookCataloguing extends Component{
    constructor(props) {
        super(props);
        this.imageID = 0;
        this.state = {
            Title:"",
            ISBN: "",
            ISBNError:false,
            Genre: "",
            Author: "",
            Pages: 0,
            Publisher:"",
            Price: 0,
            Condition:"",
            Other_details: "",
            imageArray:[],
            initImage: null,
        }
    }

    onButtonPress() {
        if (this.state.Title === "" || this.state.Condition === "" || this.state.Price === 0) {
            Alert.alert("Warning:",
                "You have to fill out Title, Condition and Price")
        } else{
            Alert.alert("BookCataloguing book: " + this.state.Title)
        }
    }

    deleteImage = (index) =>{
        const copyImageArray = Object.assign([], this.state.imageArray);
        copyImageArray.splice(index, 1)
        this.setState({
            imageArray: copyImageArray
        })
    };

    validISBN = () => {
        if ((this.state.ISBN.length !== 10) && (this.state.ISBN.length !== 13)){
            this.setState({ISBNError: true})
        } else{
            this.setState({ISBNError: false})
        }
    }

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
            <SafeAreaView style={styles.container}>
                <KeyboardAwareScrollView behavior="padding">
                {/*Create an Image Carousel*/}
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

                {/*Create other information View*/}
                <View style={{flex: 1, flexDirection: "row"}}>
                    <Text style={styles.listingTitle}>Title: </Text>
                    <Text style={styles.requiredText}>*</Text>
                </View>
                <TextInput
                    underlineColorAndroid={"transparent"}
                    style={styles.textInput}
                    clearButtonMode={"while-editing"}
                    onChangeText={(Title) => this.setState({Title})}
                />

                <Text style={styles.listingTitle}>ISBN: </Text>
                <TextInput
                    underlineColorAndroid={"transparent"}
                    style={styles.textInput}
                    keyboardType="number-pad"
                    clearButtonMode={"while-editing"}
                    maxLength={13}
                    onBlur={this.validISBN.bind(this)}
                    onChangeText={(ISBN) => this.setState({ISBN})}
                />
                    {this.state.ISBNError?
                        <Text style={{color:'red'}}>Please enter 10 or 13 digits</Text>
                        : null
                    }

                <Text style={styles.listingTitle}>Genre: </Text>
                <TextInput
                    underlineColorAndroid={"transparent"}
                    style={styles.textInput}
                    clearButtonMode={"while-editing"}
                    onChangeText={(Genre) => this.setState({Genre})}
                />

                <Text style={styles.listingTitle}>Author: </Text>
                <TextInput
                    underlineColorAndroid={"transparent"}
                    style={styles.textInput}
                    clearButtonMode={"while-editing"}
                    onChangeText={(Author) => this.setState({Author})}
                />

                <Text style={styles.listingTitle}>Page: </Text>
                <TextInput
                    underlineColorAndroid={"transparent"}
                    style={styles.textInput}
                    clearButtonMode={"while-editing"}
                    keyboardType="number-pad"
                    onChangeText={(Page) => this.setState({Page})}
                />

                <Text style={styles.listingTitle}>Publisher: </Text>
                <TextInput
                    underlineColorAndroid={"transparent"}
                    clearButtonMode={"while-editing"}
                    style={styles.textInput}
                    onChangeText={(Publisher) => this.setState({Publisher})}
                />

                <View style={{flex: 1, flexDirection: "row"}}>
                    <Text style={styles.listingTitle}>Price: </Text>
                    <Text style={styles.requiredText}>*</Text>
                </View>
                <TextInput
                    underlineColorAndroid={"transparent"}
                    style={styles.textInput}
                    clearButtonMode={"while-editing"}
                    keyboardType="number-pad"
                    onChangeText={(Price) => this.setState({Price})}
                />


                <View style={{flex: 1, flexDirection: "row"}}>
                    <Text style={styles.listingTitle}>Condition: </Text>
                    <Text style={styles.requiredText}>*</Text>
                </View>
                <RNPickerSelect
                    onValueChange={(Condition) => this.setState({Condition})}
                    style={{
                        ...pickerSelectStyles,
                        // iconContainer: {
                        // top: 20,
                        // right: 10,},
                    }}
                    items={[
                        { label: 'Brand new', value: 'Brand new' },
                        { label: 'Like new', value: 'Like new' },
                        { label: 'Very good', value: 'Very good' },
                        { label: 'Good', value: 'Good' },
                        { label: 'Acceptable', value: 'Acceptable' },
                    ]}
                    placeholder={{label: "Select a condition..."}}
                    useNativeAndroidPickerStyle={false}
                    textInputProps={{ underlineColor: 'transparent' }}
                    // Icon={() => {
                    //     return <Icon name="arrow-down" size={16} color="lightgrey" />;
                    // }}
                />

                <Text style={styles.listingTitle}>Other Details: </Text>
                <TextInput
                    underlineColorAndroid={"transparent"}
                    style={styles.textInput}
                    clearButtonMode={"while-editing"}
                    multiline={true}
                    onChangeText={(Other_details) => this.setState({Other_details})}
                />
                </KeyboardAwareScrollView>

                <TouchableOpacity
                    activityOpacity={0.5}
                    style={styles.loginButton}
                    onPress={this.onButtonPress.bind(this)}>
                    <Text style={styles.loginText}>List on eBay</Text>
                </TouchableOpacity>
            </SafeAreaView>
        )
    }
}

const pickerSelectStyles = StyleSheet.create({
    inputIOS: {
        fontSize: 16,
        paddingVertical: "2%",
        borderWidth: 1,
        borderColor: 'black',
        color: 'black',
        paddingRight: 30, // to ensure the text is never behind the icon
        padding : '2%',
        marginVertical : '2%'
    },
    inputAndroid: {
        fontSize: 16,
        paddingVertical: "2%",
        borderWidth: 1,
        borderColor: 'black',
        color: 'black',
        paddingRight: 30, // to ensure the text is never behind the icon
        padding : '2%',
        marginVertical : '2%'
    },
});

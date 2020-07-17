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
import * as Permissions from "expo-permissions";
import * as ImagePicker from "expo-image-picker";
import ShowCarousel from "./ShowCarousel";
import styles from "../config/styles";


export default class BookCataloguing extends Component{
    constructor(props) {
        super(props);
        this.imageId = 0;
        this.state = {
            title:"",
            isbn: "",
            isbnError:false,
            genre: "",
            author: "",
            pages: 0,
            publisher:"",
            price: 0,
            condition:"",
            otherDetails: "",
            imageArray:[],
            initImage: null,
        }
    }
//TODO: API call to get book data before rendering and set to state
    componentDidMount() {
        // axios.get(`http://localhost/book`)
        //     .then(res => {
        //         const data = res.data;
        //         this.setState({ title: data.title });
        //     })
    }

    onButtonPress() {
        if (this.state.title === "" || this.state.condition === "" || this.state.price === 0) {
            Alert.alert("Warning:",
                "You have to fill out Title, Condition and Price")
        } else{
            //TODO: API call to submit and redirect to RootNavigator
            Alert.alert("BookCataloguing book: " + this.state.title)
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
        if ((this.state.isbn.length !== 10) && (this.state.isbn.length !== 13)){
            this.setState({isbnError: true})
        } else{
            this.setState({isbnError: false})
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
            this.imageId = this.imageId + 1;
            const copyImageArray = Object.assign([], this.state.imageArray);
            copyImageArray.push({
                id: this.imageId,
                image: this.state.initImage
            })
            this.setState({
                imageArray: copyImageArray
            })
        }
    };
    //TODO: All fields regex check
    render() {
        return (
            <SafeAreaView style={[styles.container,{marginTop:'10%'}]}>
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
                    onChangeText={(title) => this.setState({title})}
                />

                <Text style={styles.listingTitle}>ISBN: </Text>
                <TextInput
                    underlineColorAndroid={"transparent"}
                    style={styles.textInput}
                    keyboardType="number-pad"
                    clearButtonMode={"while-editing"}
                    maxLength={13}
                    onBlur={this.validISBN.bind(this)}
                    onChangeText={(isbn) => this.setState({isbn})}
                />
                    {this.state.isbnError?
                        <Text style={{color:'red'}}>Please enter 10 or 13 digits</Text>
                        : null
                    }

                <Text style={styles.listingTitle}>Genre: </Text>
                <TextInput
                    underlineColorAndroid={"transparent"}
                    style={styles.textInput}
                    clearButtonMode={"while-editing"}
                    onChangeText={(genre) => this.setState({genre})}
                />

                <Text style={styles.listingTitle}>Author: </Text>
                <TextInput
                    underlineColorAndroid={"transparent"}
                    style={styles.textInput}
                    clearButtonMode={"while-editing"}
                    onChangeText={(author) => this.setState({author})}
                />

                <Text style={styles.listingTitle}>Page: </Text>
                <TextInput
                    underlineColorAndroid={"transparent"}
                    style={styles.textInput}
                    clearButtonMode={"while-editing"}
                    keyboardType="number-pad"
                    onChangeText={(page) => this.setState({page})}
                />

                <Text style={styles.listingTitle}>Publisher: </Text>
                <TextInput
                    underlineColorAndroid={"transparent"}
                    clearButtonMode={"while-editing"}
                    style={styles.textInput}
                    onChangeText={(publisher) => this.setState({publisher})}
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
                    onChangeText={(price) => this.setState({price})}
                />


                <View style={{flex: 1, flexDirection: "row"}}>
                    <Text style={styles.listingTitle}>Condition: </Text>
                    <Text style={styles.requiredText}>*</Text>
                </View>
                <RNPickerSelect
                    onValueChange={(condition) => this.setState({condition})}
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
                    onChangeText={(otherDetails) => this.setState({otherDetails})}
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

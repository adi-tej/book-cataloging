import React, {  Component } from 'react';
import {
    Text,
    View,
    Button,
    TextInput,
    Alert,
    TouchableOpacity,
    Dimensions,
    StyleSheet,
    ScrollView,
} from 'react-native';
import ImagePickerComponent from "./ImagePickerComponent";
import * as Permissions from "expo-permissions";
import * as ImagePicker from "expo-image-picker";
import ShowCarousel from "./ShowCarousel";

const width = Dimensions.get('window').width;

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
                            style={styles.image}
                            onPress={this.takePicture.bind(this)}>
                            <Text style={styles.buttonText}>+</Text>
                        </TouchableOpacity>
                    </ScrollView>
                </View>
                <ScrollView>
                    <Text style={styles.title}>Title: </Text>
                    <TextInput
                        underlineColorAndroid={"transparent"}
                        style={styles.text_input}
                        onChangeText={(Title) => this.setState({Title})}
                    />

                    <Text style={styles.title}>ISBN: </Text>
                    <TextInput
                        underlineColorAndroid={"transparent"}
                        style={styles.text_input}
                        keyboardType="number-pad"
                        onChangeText={(ISBN) => this.setState({ISBN})}
                    />

                    <Text style={styles.title}>Genre: </Text>
                    <TextInput
                        underlineColorAndroid={"transparent"}
                        style={styles.text_input}
                        onChangeText={(Genre) => this.setState({Genre})}
                    />

                    <Text style={styles.title}>Author: </Text>
                    <TextInput
                        underlineColorAndroid={"transparent"}
                        style={styles.text_input}
                        onChangeText={(Author) => this.setState({Author})}
                    />

                    <Text style={styles.title}>Page: </Text>
                    <TextInput
                        underlineColorAndroid={"transparent"}
                        style={styles.text_input}
                        onChangeText={(Page) => this.setState({Page})}
                    />

                    <Text style={styles.title}>Publisher: </Text>
                    <TextInput
                        underlineColorAndroid={"transparent"}
                        style={styles.text_input}
                        onChangeText={(Publisher) => this.setState({Publisher})}
                    />

                    <Text style={styles.title}>Price: </Text>
                    <TextInput
                        underlineColorAndroid={"transparent"}
                        style={styles.text_input}
                        onChangeText={(Price) => this.setState({Price})}
                    />

                    <Text style={styles.title}>Other Details: </Text>
                    <TextInput
                        underlineColorAndroid={"transparent"}
                        style={styles.text_input}
                        onChangeText={(Other_details) => this.setState({Other_details})}
                    />
                </ScrollView>

                <TouchableOpacity
                    activityOpacity={0.5}
                    style={styles.button}
                    onPress={this.onButtonPress.bind(this)}>
                    <Text style={styles.buttonText}>List on eBay</Text>
                </TouchableOpacity>
            </View>
        )
    }
}

const styles = StyleSheet.create({
    container:{
        flex:1,
        flexDirection:"column",
        justifyContent:"space-evenly"
    },
    image:{
        backgroundColor: "lightgrey",
        borderColor: "lightgrey",
        borderWidth: 0.5,
        width: width/4,
        height: width/4,
        marginHorizontal: 16,
        marginVertical: 16,
        justifyContent:'center',
        alignItems:'center'
    },
    title: {
        padding: 16,
        fontSize: 15,
        color: "black",
        fontWeight: "bold",
    },
    text_input:{
      width:width-32, //center and keep each side having 16 padding
      borderColor: "grey",
      padding:0,
      borderWidth: 1,
      alignSelf: "center",
      justifyContent:'center',
      alignItems:'center'
    },
    button:{
        width:width-32,
        height:35,
        alignSelf:'center',
        backgroundColor:'skyblue',
        marginTop:20,
        marginBottom: 20,
        justifyContent:'center',
        alignItems:'center'
        },
    buttonText:{
        fontSize: 20,
        color: "white",
        fontWeight: "bold"
    }

});

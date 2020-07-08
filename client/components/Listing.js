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

const width = Dimensions.get('window').width;

export default class Listing extends Component{
    constructor(props) {
        super(props);
        this.state = {
            Title:"",
            ISBN: "",
            Genre: "",
            Author: "",
            Pages: 0,
            Publisher:"",
            Price: 0,
            Other_details: "",
        }
    }

    onButtonPress() {
        Alert.alert("Listing book: " + this.state.Title)
    }

    render() {
        return (
            <View style={styles.container}>
                <View style={{flexDirection: "row"}}>
                    <ScrollView horizontal={true}>
                        <TouchableOpacity
                            activityOpacity={0.5}
                            style={styles.image}>
                             {/*onPress={this.onButtonPress.bind(this)}>*/}
                            <Text style={{
                                fontSize: 40,
                                color: "white",
                            }}>+</Text>
                        </TouchableOpacity>
                        <ImagePickerComponent style={styles.image} />
                        <View style={styles.image} />
                        <View style={styles.image} />
                        <View style={styles.image} />
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
                    <Text style={{
                        fontSize: 15,
                        color: "white",
                        fontWeight: "bold"
                    }}>List on eBay</Text>
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
        }

});

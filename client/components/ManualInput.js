import React, {Component} from 'react';
import {
    Text,
    View,
    SafeAreaView,
    Image, TextInput, TouchableOpacity, Alert,
    Modal,
} from 'react-native';
import {KeyboardAwareScrollView} from "react-native-keyboard-aware-scroll-view";

import styles from "../config/styles";
import images from "../config/images";
import BookCataloguing from "./BookCataloguing";
import Checkout from "./Checkout";

import api  from "../config/axios";

export default class ManualInput extends Component {
    constructor(props) {
        super(props);
        this.mode = this.props.mode
        this.state = {
            returnInfo: false, //to check if backend return information
            modalVisible:false,
            noIsbnModalVisible:false,
            isbn: "",
            isbnError:false,
            title:"",
            genre: "",
            author: "",
            pages: 0,
            publisher:"",
            price: 0,
            initImage: null,
        }
    }

    validISBN = () => {
        if ((this.state.isbn.length !== 10) && (this.state.isbn.length !== 13)){
            this.setState({isbnError: true})
        } else{
            this.setState({isbnError: false})
        }
    }


    onButtonPress = () => {
        if (this.mode === "add"){
            if (!this.state.isbnError && this.state.isbn !== "") {
                //TODO: get all info form backend and send to BookCataloguing page
                //TODO: should also check if we get the info
                Alert.alert("Go to listing page, ISBN number is: " + this.state.isbn)
            } else {
                Alert.alert("Please enter a valid ISBN number with 10 or 13 digits")
            }
        }
        else if (this.mode === "checkout") {
            if (!this.state.isbnError && this.state.isbn !== "") {
                this.setState({modalVisible: true});
            } else {
                Alert.alert("Please enter a valid ISBN number with 10 or 13 digits")
            }
        }
    }

    //TODO: get the info from backend and send to BookCataloguing page
    onTextPress = () => {
        if (this.mode === "add") {
            this.props.navigation.navigate('BookCataloguing')
        } else if (this.mode === "checkout") {
            this.setState({noIsbnModalVisible: true});
        }
    }

    // -----------------modal setting
    //TODO: pass the item ISBN to backend and request removal of this item
    onCheckoutPress = () => {
        Alert.alert("Successfully remove item from eBay!")
        setTimeout(()=>{this.setState({modalVisible: false})},1500)

        // api.post('/order/checkout', {
        //TODO:update the item details

        //   "items": [
        //     {
        //       "item_id": "string",
        //       "quantity": 0,
        //       "total_price": 0
        //     }
        //   ]
        // })
        //   .then((response) => {
        //     if (response.status === 201) {
        //         Alert.alert("Successfully remove item from eBay!")
        //         setTimeout(()=>{setModalVisible(false)},1000)
        //         setScanned(false)
        //     }
        //   })
        //   .catch(function (error) {
        //     console.warn(error);
        //     Alert.alert("Oops! You can't remove this item now! Please try it later.")
        //   });
    }

    // -----------------noIsbnModal setting
    onSearchPress = () =>{
        //TODO: After get  information, don't forget to change the returnInfo state
        //just for testing, should remove it later
        // this.setState({returnInfo: true})
        if (this.state.title === ""){
            Alert.alert("Please enter a book title")
        } else if (this.state.title !== "" && this.state.returnInfo){
            this.setState({noIsbnModalVisible:false})
            this.setState({modalVisible: true})
        } else{
            Alert.alert("Sorry, we don't have this book! You can't check it out.")
        }
    }
    // -----------------noIsbnModal setting

    render() {
        return (
            <SafeAreaView>
            <KeyboardAwareScrollView>
                <Image style={styles.manualBackground} source={images.background}/>
                <View style={styles.manualPopup}>

                    {/*closeButton*/}
                    <TouchableOpacity
                        style={styles.manualCloseButton}
                        onPress={() => {this.props.navigation.navigate('RootNavigator')}}>
                        <Text style={{ fontSize: 20, color: 'black'}}> x </Text>
                    </TouchableOpacity>

                    <Text style={styles.manualPopupTitle}>ISBN: </Text>
                    <TextInput
                        underlineColorAndroid={"transparent"}
                        style={styles.manualISBNInput}
                        keyboardType="number-pad"
                        clearButtonMode={"while-editing"}
                        maxLength={13}
                        onBlur={this.validISBN}
                        onChangeText={(isbn) => this.setState({isbn})}
                    />
                    {this.state.isbnError?
                        <Text style={{color:'red', marginLeft:"10%"}}>Please enter 10 or 13 digits</Text>
                        : null
                    }

                    {/* Create a search button*/}
                    <TouchableOpacity
                        activityOpacity={0.5}
                        style={styles.searchButton}
                        onPress={this.onButtonPress}>
                        <Text style={styles.loginText}>Search</Text>
                    </TouchableOpacity>

                    <TouchableOpacity
                        activityOpacity={0.5}
                        onPress={this.onTextPress}>
                        <Text style={styles.resetAccountButton}>No ISBN?</Text>
                    </TouchableOpacity>
                </View>
            </KeyboardAwareScrollView>

                {/*---------------------popup for checkout------*/}
                <Modal
                    transparent={true}
                    visible={this.state.modalVisible}
                >
                    <View style={{backgroundColor:"#000000aa", flex: 1}}>
                        <View style={styles.checkoutPopup}>
                            <View style={{paddingVertical:"10%",}}>
                                {/*TODO: pass bookCover, title, author and price to it*/}
                                <Checkout />
                                <View style={styles.buttonView}>
                                    <TouchableOpacity
                                        activityOpacity={0.5}
                                        style={styles.removeButton}
                                        onPress={this.onCheckoutPress}>
                                        <Text style={styles.loginText}>Checkout item</Text>
                                    </TouchableOpacity>
                                    <TouchableOpacity
                                        activityOpacity={0.5}
                                        style={[styles.removeButton, {backgroundColor: "lightgrey"}]}
                                        onPress={()=>this.setState({modalVisible: false})}>
                                        <Text style={styles.loginText}>Close</Text>
                                    </TouchableOpacity>
                                </View>
                            </View>
                        </View>
                    </View>
                </Modal>
                {/*---------------------popup for checkout*/}

                {/*---popup for no ISBN*/}
                <Modal
                    transparent={true}
                    visible={this.state.noIsbnModalVisible}
                >
                    <View style={styles.modalView}>
                        <View style={styles.noIsbnPopup}>
                            <View style={{paddingVertical:"10%",}}>
                                <TextInput
                                    placeholder='Please enter a book title'
                                    underlineColorAndroid={"transparent"}
                                    style={[styles.textInput, {margin: "5%",width:"90%"}]}
                                    clearButtonMode={"while-editing"}
                                    onChangeText={(title) => this.setState({title})}
                                />

                                <View style={styles.buttonView}>
                                    <TouchableOpacity
                                        activityOpacity={0.5}
                                        style={styles.removeButton}
                                        onPress={this.onSearchPress}>
                                        <Text style={styles.loginText}>Search</Text>
                                    </TouchableOpacity>
                                    <TouchableOpacity
                                        activityOpacity={0.5}
                                        style={[styles.removeButton, {backgroundColor: "lightgrey"}]}
                                        onPress={()=>this.setState({noIsbnModalVisible: false})}>
                                        <Text style={styles.loginText}>Close</Text>
                                    </TouchableOpacity>
                                </View>
                            </View>
                        </View>
                    </View>
                </Modal>

                {/*---popup for no ISBN*/}


            </SafeAreaView>
        );
    }
}

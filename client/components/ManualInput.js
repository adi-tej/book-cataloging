import React, {Component} from 'react';
import {
    Text,
    View,
    SafeAreaView,
    Image, TextInput, TouchableOpacity, Alert,
} from 'react-native';
import {KeyboardAwareScrollView} from "react-native-keyboard-aware-scroll-view";
import styles from "../config/styles";
import images from "../config/images";

export default class ManualInput extends Component {
    constructor(props) {
        super(props);
        this.state = {
            isbn: "",
            isbnError:false,
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
        Alert.alert("ISBN number is: " + this.state.isbn)
    }

    render() {
        return (
            <SafeAreaView>
            <KeyboardAwareScrollView>
                <Image style={styles.manualBackground} source={images.bookCover}/>
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
                        onBlur={this.validISBN.bind(this)}
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
                        onPress={this.onButtonPress.bind(this)}>
                        <Text style={styles.loginText}>Search</Text>
                    </TouchableOpacity>
                    <TouchableOpacity
                        activityOpacity={0.5}
                        onPress={()=>{this.props.navigation.navigate('BookCataloguing')}}>
                        <Text style={styles.resetAccountButton}>No ISBN</Text>
                    </TouchableOpacity>
                </View>

            </KeyboardAwareScrollView>
            </SafeAreaView>
        );
    }
}

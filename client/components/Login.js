import React from 'react';
import { Button, Text, View, Image, TextInput,StyleSheet } from 'react-native';
import logo from "../assets/Rectangle614.png";
export default function Login({navigation}){
    return(
        <View>
            <Image source={logo} style={styles.image}/>
            <View style={styles.container}>
                <TextInput placeholder='Username' style={styles.textInput}/>
                <TextInput placeholder='Password' style={styles.textInput}/>
                <Button onPress={() => navigation.navigate('TabNavigator')} title="Login" style={styles.button}/>
            </View>
        </View>
    )
}

const styles = StyleSheet.create({
    container : {
        marginTop : '50%'
    },
    image:{
        marginTop : '20%',
        alignSelf : 'center'
    },
    textInput : {
        width : '100%',
        borderColor: 'black',
        paddingHorizontal : '10%',
        borderWidth: 1,
        fontSize : 16,
        margin : '1%',
        marginLeft : 0,
        padding : '1%'
    },
    button:{
        padding : '1%'
    }
})

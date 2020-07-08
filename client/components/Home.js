import React from 'react';
import { Text, View, Button } from 'react-native';
import Login from "./Login";
import styles from "../config/styles";
export default function Home({navigation}){
    return(
        <View style={styles.container}>
            <Button onPress={()=>navigation.navigate('Camera')} title="Camera" />
            <Button onPress={()=>navigation.navigate('Barcode')} title="Barcode"/>
            <Button onPress={()=>navigation.navigate('TestImage')} title="Test"/>
            <Login navigation={navigation}/>
        </View>
    )
}

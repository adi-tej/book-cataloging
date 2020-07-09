import React from 'react';
import {  View } from 'react-native';
import Login from "./Login";
import styles from "../config/styles";
export default function Home({navigation}){
    return(
        <View style={styles.container}>
            <Login navigation={navigation}/>
        </View>
    )
}

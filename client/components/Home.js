import React from 'react';
import {StyleSheet, Text, View} from 'react-native';
import Login from "./Login";
export default function Home({navigation}){
    return(
        <View style={styles.container}>
            <Text>
                This is Home Component.
            </Text>
            <Login navigation={navigation}/>
        </View>
    )

}
const styles = StyleSheet.create({
    container : {
        flex : 1,
        margin : '5%'
    }
})

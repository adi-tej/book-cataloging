import React from 'react';
import { Text, View } from 'react-native';
import Login from "./Login";
export default function Home({navigation}){
    return(
        <View>
            <Text>
                This is Home Component.
            </Text>
            <Login navigation={navigation}/>
        </View>
    )

}

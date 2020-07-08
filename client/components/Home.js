import React from 'react';
import { Text, View, Button } from 'react-native';
import Login from "./Login";
export default function Home({navigation}){
    return(
        <View>
            <Text>
                This is Home Component
            </Text>
            <Button onPress={()=>navigation.navigate('Camera')} title="Camera"></Button>
            <Login navigation={navigation}/>
        </View>
    )

}

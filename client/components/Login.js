import React from 'react';
import { Button, Text, View } from 'react-native';
export default function Login({navigation}){
    return(
        <View>
            <Text>This is Login screen.</Text>
            <Button onPress={() => navigation.navigate('TabNavigator')} title="Login"/>
        </View>
    )
}

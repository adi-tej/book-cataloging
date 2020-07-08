import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createStackNavigator } from '@react-navigation/stack';

import Home from "./components/Home";
import DrawerNavigator from "./components/DrawerNavigator";
import Barcode from "./components/Barcode";
import Listing from "./components/Listing";
import ImagePickerComponent from "./components/ImagePickerComponent";

const Stack = createStackNavigator();

export default function App(){
  return (
        <NavigationContainer>
            <Stack.Navigator initialRouteName="Home" screenOptions={{
                headerShown: false
            }}>
                <Stack.Screen name="Landing" component={Home}/>
                <Stack.Screen name="rootNavigator" component={DrawerNavigator} />
                <Stack.Screen name="Barcode" component={Barcode}/>
                <Stack.Screen name="Camera" component={ImagePickerComponent}/>
            </Stack.Navigator>
        </NavigationContainer>
  );

}

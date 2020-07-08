import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createStackNavigator } from '@react-navigation/stack';
import { MenuProvider } from 'react-native-popup-menu';
import Home from "./components/Home";
import DrawerNavigator from "./components/DrawerNavigator";
import Barcode from "./components/Barcode";
import Listing from "./components/Listing";
import ImagePickerComponent from "./components/ImagePickerComponent";

import Scanner from "./components/Scanner";
import CameraTabNavigator from "./components/CameraTabNavigator";
const Stack = createStackNavigator();

export default function App(){
  return (
      <MenuProvider>
        <NavigationContainer>
            <Stack.Navigator initialRouteName="Home" screenOptions={{
                headerShown: false
            }}>
                <Stack.Screen name="Landing" component={Home}/>
                <Stack.Screen name="RootNavigator" component={DrawerNavigator} />
                <Stack.Screen name="CameraTab" component={CameraTabNavigator} />
                <Stack.Screen name="Barcode" component={Barcode}/>
                <Stack.Screen name="Camera" component={ImagePickerComponent}/>
            </Stack.Navigator>
        </NavigationContainer>
      </MenuProvider>
  );
}

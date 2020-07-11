import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createStackNavigator } from '@react-navigation/stack';
import { MenuProvider } from 'react-native-popup-menu';
import Home from "./components/Home";
import DrawerNavigator from "./components/DrawerNavigator";

import CameraTabNavigator from "./components/CameraTabNavigator";
import BookCataloguing from "./components/BookCataloguing";
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
                <Stack.Screen name="BookCataloguing" component={BookCataloguing}/>
            </Stack.Navigator>
        </NavigationContainer>
      </MenuProvider>
  );
}

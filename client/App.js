import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createStackNavigator } from '@react-navigation/stack';

import Home from "./components/Home";
import DrawerNavigator from "./components/DrawerNavigator";

const Stack = createStackNavigator();

export default function App(){
  return (
        <NavigationContainer>
            <Stack.Navigator initialRouteName="Home" screenOptions={{
                headerShown: false
            }}>
                <Stack.Screen name="Landing" component={Home}/>
                <Stack.Screen name="rootNavigator" component={DrawerNavigator} />
            </Stack.Navigator>
        </NavigationContainer>
  );

}

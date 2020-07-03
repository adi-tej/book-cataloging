import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createStackNavigator } from '@react-navigation/stack';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import 'react-native-gesture-handler';

import Home from "./components/Home";
import Cataloging from "./components/Cataloging";
const Stack = createStackNavigator();
const Tab = createBottomTabNavigator()

function TabNavigator(){
    return(
        <Tab.Navigator>
            <Tab.Screen name='Cataloging' component={Cataloging} />
            <Tab.Screen name='Dashboard' component={Cataloging} />
        </Tab.Navigator>
    )
}

export default function App(){
  return (
      <NavigationContainer>
        <Stack.Navigator
            // screenOptions={{
            //   headerStyle: {
            //     backgroundColor: '#f4511e',
            //   },
            //   headerTintColor: '#fff',
            //   headerTitleStyle: {
            //     fontWeight: 'bold',
            //   },
            // }}
            >
          <Stack.Screen name="Home" component={Home}/>
          <Stack.Screen name="TabNavigator" component={TabNavigator} />
        </Stack.Navigator>
      </NavigationContainer>
  );
}

import React from 'react';
import {View} from 'react-native';
import {createDrawerNavigator} from "@react-navigation/drawer";
import Logout from "./Logout";
import TabNavigator from "./TabNavigator";
const Drawer = createDrawerNavigator()
export default function DrawerNavigator(){
    return(
        <View style={{flex:1}}>
                <Drawer.Navigator initialRouteName="UserHome">
                    <Drawer.Screen name="Dashboard" component={TabNavigator} options={{ drawerLabel: 'Dashboard' }}/>
                    <Drawer.Screen name="Logout" component={Logout} options={{ drawerLabel: 'Logout' }}/>
                </Drawer.Navigator>
        </View>
    )
}

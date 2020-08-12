import React from 'react';
import {View} from 'react-native';
import {createDrawerNavigator} from "@react-navigation/drawer";
import colors from '../../config/colors';
import Logout from "../Logout";
import TabNavigator from "./TabNavigator";
import CustomDrawer from "./CustomDrawer";
import Home from "../Home";

const Drawer = createDrawerNavigator()
export default function DrawerNavigator(){
    return(
        <View style={{flex:1}}>
                <Drawer.Navigator initialRouteName="UserHome" drawerContentOptions={{
                    inactiveTintColor : 'white',
                    activeTintColor : 'white',
                    style:{
                        backgroundColor: colors.drawer
                    }
                }} drawerContent={props => <CustomDrawer {...props} />}>
                    <Drawer.Screen name="Dashboard" component={TabNavigator} options={{ drawerLabel: 'Dashboard' }}/>
                    <Drawer.Screen name="Logout" component={Home} options={{ drawerLabel: 'Logout' }}/>
                </Drawer.Navigator>
        </View>
    )
}

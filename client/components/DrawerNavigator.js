import React from 'react';
import {View} from 'react-native';
import {createDrawerNavigator} from "@react-navigation/drawer";
import colors from '../config/colors';
import Logout from "./Logout";
import TabNavigator from "./TabNavigator";
import Login from "./Login"
import CustomDrawer from "./CustomDrawer";
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
                    <Drawer.Screen name="Logout" component={Login} options={{ drawerLabel: 'Logout' }}/>
                    {/*<Drawer.Screen name="Logout" component={Login}/>*/}
                </Drawer.Navigator>
        </View>
    )
}

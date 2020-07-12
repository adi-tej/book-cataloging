import React from 'react';
import {createBottomTabNavigator} from "@react-navigation/bottom-tabs";
import { View} from 'react-native';
import Scanner from "./BarcodeScanner";
import ManualInput from "./ManualInput";
import Logout from "./Logout";
import styles from "../config/styles";

const Tab = createBottomTabNavigator()
export default function CameraTabNavigator(){
    return(
        <View  style={{flex:1, backgroundColor: 'transparent',}}>
            <Tab.Navigator initialRouteName="Barcode" tabBarOptions={{
                inactiveBackgroundColor:'rgba(0,0,0,0.5)',
                activeBackgroundColor : 'rgba(0,0,0,0.8)',
                activeTintColor:'white',
                tabStyle:styles.cameraScanTab,
                labelStyle:styles.cameraScanTabLabel,
                style:styles.cameraScanTabNavigator
            }}>
                <Tab.Screen name="Barcode" component={Scanner}/>
                <Tab.Screen name="OCR" component={Logout}/>
                <Tab.Screen name="Manual" component={ManualInput}/>
            </Tab.Navigator>
        </View>
    )
}

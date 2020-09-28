import React from 'react';
import {createBottomTabNavigator} from "@react-navigation/bottom-tabs";
import { View} from 'react-native';
import Scanner from "../BarcodeScanner";
import ManualInput from "../ManualInput";
import styles from "../../config/styles";
import OcrScanner2 from "../OcrScanner";

const Tab = createBottomTabNavigator()

export default function CameraTabNavigator({navigation,route}){

    const { mode } = route.params;

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
                <Tab.Screen name="Barcode" children={()=> <Scanner mode={mode} navigation={navigation}/>} />
                <Tab.Screen name="OCR" children={()=> <OcrScanner2 mode={mode} navigation={navigation}/>} />
                <Tab.Screen name="Manual" children={()=> <ManualInput mode={mode} navigation={navigation}/>}/>

            </Tab.Navigator>
        </View>
    )
}

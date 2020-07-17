import React, {Component} from 'react';
import {View, Text, TouchableOpacity} from 'react-native';
import { createMaterialTopTabNavigator } from '@react-navigation/material-top-tabs';
import {
    Menu,
    MenuOptions,
    MenuOption,
    MenuTrigger,
} from 'react-native-popup-menu';
import styles from "../config/styles";
import BookCataloguing from "./BookCataloguing";
import PendingOrders from "./PendingOrders";
import ActiveListing from "./ActiveListing";
import TabHeader from "./TabHeader";
const Tab = createMaterialTopTabNavigator()

export default class TabNavigator extends Component{
    render(){
    return(
        <View style={{flex:1}}>
            <TabHeader navigation={this.props.navigation}/>
            <Tab.Navigator initialRouteName="Cataloging">
                <Tab.Screen name="Active Listing" component={ActiveListing} />
                <Tab.Screen name="Pending Orders" component={PendingOrders} />
                <Tab.Screen name="Test tab" component={BookCataloguing} />
            </Tab.Navigator>
            {/*<TouchableOpacity*/}
            {/*    style={styles.checkoutButton}>*/}
            {/*    <Text style={{ fontSize: 24, color: 'white'}}>Checkout</Text>*/}
            {/*</TouchableOpacity>*/}
        </View>
    )}
}

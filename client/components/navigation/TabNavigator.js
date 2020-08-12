import React, {Component} from 'react';
import {View, Text, TouchableOpacity} from 'react-native';
import { createMaterialTopTabNavigator } from '@react-navigation/material-top-tabs';
import Orders from "../Orders";
import ActiveListing from "../ActiveListing";
import TabHeader from "../TabHeader";

import styles from "../../config/styles";

const Tab = createMaterialTopTabNavigator()

export default class TabNavigator extends Component{

    render(){
    return(
        <View style={{flex:1}}>
            <TabHeader navigation={this.props.navigation}/>
            <Tab.Navigator initialRouteName="Cataloging">
                <Tab.Screen name="Active Listing" component={ActiveListing} />
                <Tab.Screen name="Pending Orders" children={() => <Orders mode={"pending"} navigation={this.props.navigation} params={this.props.route.params}/>} />
                <Tab.Screen name="Accepted Orders" children={() => <Orders mode={"confirmed"} navigation={this.props.navigation} params={this.props.route.params}/>}/>

            </Tab.Navigator>
            <TouchableOpacity
                onPress={() => this.props.navigation.navigate('CameraTab', {mode: "checkout"})}
                style={styles.checkoutButton}>
                <Text style={{ fontSize: 24, color: 'white'}}>Checkout</Text>
            </TouchableOpacity>
        </View>
    )}
}

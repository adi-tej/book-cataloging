import React, {Component} from 'react';
import {View} from 'react-native';
import {Header, Left, Right, Icon} from "native-base";
import { createMaterialTopTabNavigator } from '@react-navigation/material-top-tabs';
import { withNavigation, DrawerActions } from 'react-navigation'
import Cataloging from "./Cataloging";

const Tab = createMaterialTopTabNavigator()
export default class TabNavigator extends Component{
    render(){
    return(
        <View style={{flex:1}}>
            <Header style={{backgroundColor:'white'}}>
                <Left style={{flex:1}}>
                    <Icon onPress={() => this.props.navigation.toggleDrawer()} name='menu'/>
                </Left>
            </Header>
            <Tab.Navigator initialRouteName="Cataloging">
                <Tab.Screen name="Active Listing" component={Cataloging} />
                <Tab.Screen name="Pending Orders" component={Cataloging} />
            </Tab.Navigator>
        </View>
    )}
}

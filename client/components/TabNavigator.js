import React, {Component} from 'react';
import {View, Text, TouchableOpacity} from 'react-native';
import {Header, Left, Right, Icon} from "native-base";
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
import ActiveListingTab from "./ActiveListingTab";

const Tab = createMaterialTopTabNavigator()

export default class TabNavigator extends Component{
    render(){
    return(
        <View style={{flex:1}}>
            <Header style={{backgroundColor:'white'}}>
                <Left>
                    <Icon onPress={() => this.props.navigation.toggleDrawer()} name='menu' style={{marginHorizontal:'5%'}}/>
                </Left>
                <Right>
                    <Icon name='search' style={{marginHorizontal:'8%'}}/>
                    <Menu>
                        <MenuTrigger>
                            <Icon name="add" style={{marginHorizontal:'8%'}}/>
                        </MenuTrigger>
                        <MenuOptions optionsContainerStyle={styles.contextMenuContainer}>
                            <MenuOption onSelect={() => this.props.navigation.navigate('CameraTab')}>
                                {/*<TouchableOpacity*/}
                                {/*    style={{*/}
                                {/*        flex:1,*/}
                                {/*        justifyContent:'center',*/}
                                {/*        backgroundColor:'grey',*/}
                                {/*        alignItems:'center',*/}
                                {/*        padding:'5%'*/}
                                {/*    }}*/}
                                {/*    >*/}

                                <Text style={styles.contextMenuText}>List a book</Text>
                                {/*</TouchableOpacity>*/}
                            </MenuOption>
                            <MenuOption>
                                <Text style={styles.contextMenuText}>List clothing</Text>
                                {/*<TouchableOpacity*/}
                                {/*    style={{*/}
                                {/*        flex:1,*/}
                                {/*        justifyContent:'center',*/}
                                {/*        backgroundColor:'grey',*/}
                                {/*        alignItems:'center',*/}
                                {/*        padding:'5%'*/}
                                {/*    }}>*/}
                                {/*    <Text style={{ fontSize: 24, color: 'white'}}>List clothing</Text>*/}
                                {/*</TouchableOpacity>*/}
                            </MenuOption>
                        </MenuOptions>
                    </Menu>
                </Right>
            </Header>
            <Tab.Navigator initialRouteName="Cataloging">
                <Tab.Screen name="Active Listing" component={ActiveListingTab} />
                <Tab.Screen name="Pending Orders" component={PendingOrders} />
                <Tab.Screen name="Test tab" component={BookCataloguing} />
            </Tab.Navigator>
            <TouchableOpacity
                style={styles.checkoutButton}>
                <Text style={{ fontSize: 24, color: 'white'}}>Checkout</Text>
            </TouchableOpacity>
        </View>
    )}
}

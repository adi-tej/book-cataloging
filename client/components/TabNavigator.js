import React, {Component} from 'react';
import {View, Text, TouchableOpacity} from 'react-native';
import {Header, Left, Right, Icon} from "native-base";
import { createMaterialTopTabNavigator } from '@react-navigation/material-top-tabs';
import { withNavigation, DrawerActions } from 'react-navigation'
import {
    Menu,
    MenuOptions,
    MenuOption,
    MenuTrigger,
} from 'react-native-popup-menu';
import Cataloging from "./Cataloging";
import styles from "../config/styles";

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
                            <Icon type="AntDesign" name="plus" style={{marginHorizontal:'8%'}}/>
                        </MenuTrigger>
                        <MenuOptions
                            optionsContainerStyle={styles.contextMenuContainer}
                            customStyles={{
                                backgroundColor:'transparent'
                            }}>
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
                <Tab.Screen name="Active Listing" component={Cataloging} />
                <Tab.Screen name="Pending Orders" component={Cataloging} />
            </Tab.Navigator>
            <TouchableOpacity
                style={styles.checkoutButton}>
                <Text style={{ fontSize: 24, color: 'white'}}>Checkout</Text>
            </TouchableOpacity>
        </View>
    )}
}

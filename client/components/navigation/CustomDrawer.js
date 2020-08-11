import React from 'react';
import {DrawerContentScrollView, DrawerItemList, DrawerItem} from "@react-navigation/drawer";
export default function CustomDrawer(props) {
    return (
        <DrawerContentScrollView {...props} >
            <DrawerItem label="LOGO NAME" labelStyle={{color:'white'}} onPress={}/>
            <DrawerItemList {...props} />
        </DrawerContentScrollView>
    );
}

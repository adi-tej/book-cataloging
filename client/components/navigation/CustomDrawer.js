import React from 'react';
import {DrawerContentScrollView, DrawerItemList, DrawerItem} from "@react-navigation/drawer";
export default function CustomDrawer(props) {
    return (
        <DrawerContentScrollView {...props} >
            <DrawerItem label="USER INFO" labelStyle={{color:'white'}}/>
            <DrawerItemList {...props} />
        </DrawerContentScrollView>
    );
}

import React, { useState, useEffect } from 'react';
import {Text, View, StyleSheet, TouchableOpacity, Modal, SafeAreaView, Alert} from 'react-native';
import { BarCodeScanner } from 'expo-barcode-scanner';
import styles from "../config/styles";
import {Camera} from "expo-camera";
import Checkout from "./Checkout";

import api  from "../config/axios";

export default function Barcode({navigation,mode}) {

    const [hasPermission, setHasPermission] = useState(null);
    const [scanned, setScanned] = useState(false);
    const [type, setType] = useState(Camera.Constants.Type.back);
    // const [flashMode,setFlashMode] = useState(Camera.Constants.FlashMode.auto);
    const [modalVisible, setModalVisible] = useState(false);

    const [barcode, setBarcode] = useState("");
    // const [title, setTitle] = useState("");
    // const [genre, setGenre] = useState("");
    // const [author, setAuthor] = useState("");
    // const [pages, setPages] = useState(0);
    // const [publisher, setPublisher] = useState("");
    // const [price, setPrice] = useState(0);
    // const [initImage, setInitImage] = useState(null);


    useEffect(() => {
        (async () => {
            const { status } = await BarCodeScanner.requestPermissionsAsync();
            setHasPermission(status === 'granted');
        })();
    }, []);

    const handleBarCodeScanned = ({ type, data }) => {
        setScanned(true);
        setBarcode(data);
        //TODO: redirect to book cataloging page with barcode/isbn as prop
        if (mode === "add") {
            console.warn(`Go to listing page: Bar code with type ${type} and data ${data} has been scanned!`);
            navigation.navigate('BookCataloguing', {isbn: data})
        } else if (mode === "checkout"){
            setModalVisible(true);
        }
    };

    // -----------------modal setting
    //TODO: API call to pass the item item_id to backend and request removal of this item
    const onCheckoutPress = (() => {
        Alert.alert("Successfully remove item from eBay!")
        setTimeout(()=>{setModalVisible(false)},1000)
        setScanned(false)

        // api.post('/order/checkout', {
        //TODO:update the item details

        //   "items": [
        //     {
        //       "item_id": "string",
        //       "quantity": 0,
        //       "total_price": 0
        //     }
        //   ]
        // })
        //   .then((response) => {
        //     if (response.status === 201) {
        //         Alert.alert("Successfully remove item from eBay!")
        //         setTimeout(()=>{setModalVisible(false)},1000)
        //         setScanned(false)
        //     }
        //   })
        //   .catch(function (error) {
        //     console.warn(error);
        //     Alert.alert("Oops! You can't remove this item now! Please try it later.")
        //   });

    });
    // -----------------modal setting

    if (hasPermission === null) {
        return <Text>Requesting for camera permission</Text>;
    }
    if (hasPermission === false) {
        return <Text>No access to camera</Text>;
    }

    return (
        <View
            style={styles.cameraComponent}>
            <BarCodeScanner
                onBarCodeScanned={scanned ? undefined : handleBarCodeScanned}
                style={StyleSheet.absoluteFillObject}
                type={type}
                // flashMode={flashMode}
            >
                <View
                    style={styles.barcodeCameraComponent}>
                    <TouchableOpacity
                        style={[styles.cameraOption,{
                            width:'8%',
                            marginLeft : '3%'
                        }]}
                        onPress={() => navigation.navigate('RootNavigator')}>
                        <Text style={{ fontSize: 18, color: 'white'}}> X </Text>
                    </TouchableOpacity>
                    {/*<TouchableOpacity*/}
                    {/*    style={[styles.cameraOption,{*/}
                    {/*        width:'22%',*/}
                    {/*        marginLeft : '3%'*/}
                    {/*    }]}*/}
                    {/*    onPress={() => {*/}
                    {/*        setFlashMode(*/}
                    {/*            flashMode === Camera.Constants.FlashMode.auto*/}
                    {/*                ? Camera.Constants.FlashMode.on*/}
                    {/*                : flashMode === Camera.Constants.FlashMode.on*/}
                    {/*                ? Camera.Constants.FlashMode.off*/}
                    {/*                : Camera.Constants.FlashMode.auto*/}
                    {/*        );*/}
                    {/*    }}>*/}
                    {/*    <Text style={{ fontSize: 18, color: 'white' }}> Flash </Text>*/}
                    {/*</TouchableOpacity>*/}
                    <TouchableOpacity
                        style={[styles.cameraOption,{
                            width:'35%',
                            marginLeft : '27%'
                        }]}
                        onPress={() => {
                            setType(
                                type === Camera.Constants.Type.back
                                    ? Camera.Constants.Type.front
                                    : Camera.Constants.Type.back
                            );
                        }}>
                        <Text style={{ fontSize: 18, color: 'white' }}> Switch Cam </Text>
                    </TouchableOpacity>

                </View>
            </BarCodeScanner>

            {/*---------------------popup for checkout------*/}
            <Modal
                transparent={true}
                visible={modalVisible}
            >
                <View style={{backgroundColor:"#000000aa", flex: 1}}>
                    <View style={styles.checkoutPopup}>
                        <View style={{paddingVertical:"10%",}}>
                            {/*TODO: pass bookCover, title, author and price to it*/}
                            <Checkout />
                            <View style={styles.buttonView}>
                                <TouchableOpacity
                                    activityOpacity={0.5}
                                    style={styles.removeButton}
                                    onPress={onCheckoutPress}>
                                    <Text style={styles.loginText}>Checkout item</Text>
                                </TouchableOpacity>
                                <TouchableOpacity
                                    activityOpacity={0.5}
                                    style={[styles.removeButton, {backgroundColor: "lightgrey"}]}
                                    onPress={()=>{setModalVisible(false)
                                        setScanned(false)
                                    }}>
                                    <Text style={styles.loginText}>Close</Text>
                                </TouchableOpacity>
                            </View>
                        </View>
                    </View>
                </View>
            </Modal>
            {/*---------------------popup for checkout*/}
        </View>
    );
}

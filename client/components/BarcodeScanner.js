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
    const [modalVisible, setModalVisible] = useState(false);

    const [barcode, setBarcode] = useState("");
    // const [title, setTitle] = useState("");
    // // const [genre, setGenre] = useState("");
    // const [author, setAuthor] = useState("");
    // // const [pages, setPages] = useState(0);
    // // const [publisher, setPublisher] = useState("");
    // const [price, setPrice] = useState(0);
    // const [initImage, setInitImage] = useState(null);

    const [book, setBook] = useState(null);


    //access camera permission
    useEffect(() => {
        (async () => {
            const { status } = await BarCodeScanner.requestPermissionsAsync();
            setHasPermission(status === 'granted');
        })();
    }, []);

    if (hasPermission === null) {
        return <Text>Requesting for camera permission</Text>;
    }
    if (hasPermission === false) {
        return <Text>No access to camera</Text>;
    }

    const handleBarCodeScanned = ({ type, data }) => {
        setScanned(true);
        setBarcode(data);
        //TODO: redirect to book cataloging page with barcode/isbn as prop
        if (mode === "add") {
            // Alert.alert(`Searching for isbn ${data} ...`)
            // console.warn(`Go to listing page: Bar code with type ${type} and data ${data} has been scanned!`);
            setScanned(false)
            setTimeout( ()=> {navigation.navigate('BookCataloguing', {isbn: data}) }, 2000)
        } else if (mode === "checkout"){

            api.get('/book', {
                    params: {
                        isbn: data
                    }
            })
                .then(response => {
                        if(response.status === 200) {
                            const info = response.data.books[0]
                            if (info !== undefined) {
                                setBook(info)
                                setModalVisible(true)
                            } else {
                                Alert.alert("Sorry, we don't have this book! You can't check it out.")
                            }
                        }
                    }).catch((error) => {
                        Alert.alert("Sorry, we don't have this book! You can't check it out.")
                })
        }
    };

    // -----------------checkout modal setting ---------------------
    //TODO: API call to request removal of this item
    const onCheckoutPress = (() => {
         console.warn("book info: ", book.id)

        api.post('/order/checkout', {
          items: [
            {
              item_id: book.id,
              quantity: 1,
            }
          ]
        })
          .then((response) => {
            if (response.status === 200) {
                Alert.alert("Successfully remove item from eBay!")
                const info = response.data.items[0]
                info.total_price = info.price
                setTimeout(()=>{setModalVisible(false)},1000)
                setBook(info)
                setScanned(false)
            } else {
                Alert.alert("Oops! You can't remove this item now! Please try it later.")
            }
          })
          .catch(function (error) {
            Alert.alert("Oops! You can't remove this item now! Please try it later.")
          });
    });
    // -----------------modal setting


    return (
        //setting layout of barcode scanner page
        <View
            style={styles.cameraComponent}>
            <BarCodeScanner
                onBarCodeScanned={scanned ? undefined : handleBarCodeScanned}
                style={StyleSheet.absoluteFillObject}
                type={type}
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

            {/*---------------------setting popup window for checkout------*/}
            <Modal
                transparent={true}
                visible={modalVisible}
            >
                <View style={{backgroundColor:"#000000aa", flex: 1}}>
                    <View style={styles.checkoutPopup}>
                        <View style={{paddingVertical:"10%",}}>
                            {/*TODO: pass bookCover, title, author and price to it*/}
                            <Checkout book={book}/>
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

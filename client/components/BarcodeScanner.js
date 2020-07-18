import React, { useState, useEffect } from 'react';
import {Text, View, StyleSheet, Button, TouchableOpacity} from 'react-native';
import { BarCodeScanner } from 'expo-barcode-scanner';
import styles from "../config/styles";
import {Camera} from "expo-camera";

export default function Barcode({navigation}) {
    const [hasPermission, setHasPermission] = useState(null);
    const [scanned, setScanned] = useState(false);
    const [type, setType] = useState(Camera.Constants.Type.back);
    const [flashMode,setFlashMode] = useState(Camera.Constants.FlashMode.auto);
    const [barcode, setBarcode] = useState("");

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
        alert(`Bar code with type ${type} and data ${data} has been scanned!`);
    };

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
                flashMode={flashMode}
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
                            width:'22%',
                            marginLeft : '3%'
                        }]}
                        onPress={() => {
                            setFlashMode(
                                flashMode === Camera.Constants.FlashMode.auto
                                    ? Camera.Constants.FlashMode.on
                                    : flashMode === Camera.Constants.FlashMode.on
                                    ? Camera.Constants.FlashMode.off
                                    : Camera.Constants.FlashMode.auto
                            );
                        }}>
                        <Text style={{ fontSize: 18, color: 'white' }}> Flash </Text>
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

            {/*{scanned && (*/}
            {/*    <Button*/}
            {/*        style={{*/}
            {/*            backgroundColor:'blue',*/}
            {/*            position: "absolute",*/}
            {/*            bottom: 30}}*/}
            {/*        title={'Tap to Scan Again'}*/}
            {/*        onPress={() => setScanned(false)} />*/}
            {/*)}*/}
        </View>
    );
}

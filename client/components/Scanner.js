import React,{useState,useEffect} from 'react';
import {Camera} from 'expo-camera';
import { Text, View,TouchableOpacity} from 'react-native';
import styles from '../config/styles';
export default function Scanner({navigation}) {
    const [hasPermission, setHasPermission] = useState(null);
    const [type, setType] = useState(Camera.Constants.Type.back);
    const [flashMode,setFlashMode] = useState(Camera.Constants.FlashMode.auto)
    useEffect(() => {
        (async () => {
            const { status } = await Camera.requestPermissionsAsync();
            setHasPermission(status === 'granted');
        })();
    }, []);

    if (hasPermission === null) {
        return <View />;
    }
    if (hasPermission === false) {
        return <Text>No access to camera</Text>;
    }
    return (
        <View style={{ flex: 1 }}>
            <Camera style={{ flex: 1 }} type={type} flashMode={flashMode}>
                <View
                    style={{
                        flex: 1,
                        backgroundColor: 'transparent',
                        flexDirection:'row'
                    }}>
                    <TouchableOpacity
                        style={[styles.cameraOption,{
                            width:'8%',
                            marginLeft : '3%'
                        }]}
                        onPress={() => navigation.navigate('RootNavigator')}>
                        <Text style={{ fontSize: 30, color: 'white'}}> X </Text>
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
            </Camera>
        </View>
    );
}

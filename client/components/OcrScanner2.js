import * as React from 'react';
import { Button, Image, View, Platform } from 'react-native';
import * as ImagePicker from 'expo-image-picker';
import * as Permissions from 'expo-permissions';

export default class OcrScanner2 extends React.Component {
    state = {
        image: null,
    };

    takePicture = async() => {
        await Permissions.askAsync(Permissions.CAMERA);
        const {cancelled, uri} = await ImagePicker.launchCameraAsync({
            allowsEditing: true,
            aspect: [4,3],
            quality: 1
        });
        if (!cancelled) {
            this.setState({image: uri});
        }
    };

    render() {
        let { image } = this.state;

        return (
            <View style={{ flex: 1, alignItems: 'center', justifyContent: 'center' }}>
                <Button title="Pick an image from camera roll" onPress={this._pickImage} />
                {image && <Image source={{ uri: image }} style={{ width: 200, height: 200 }} />}
                <Button title="Go to Camera" onPress={this.takePicture.bind(this)} />
                {image && <Image source={{ uri: image }} style={{ width: 200, height: 200 }} />}
            </View>
        );
    }

    componentDidMount() {
        this.getPermissionAsync();
    }

    getPermissionAsync = async () => {
        if (Platform.OS !== 'web') {
            const { status } = await Permissions.askAsync(Permissions.CAMERA_ROLL);
            if (status !== 'granted') {
                alert('Sorry, we need camera roll permissions to make this work!');
            }
        }
    };

    _pickImage = async () => {
        try {
            let result = await ImagePicker.launchImageLibraryAsync({
                allowsEditing: true,
                aspect: [4, 3],
                quality: 1,
            });
            if (!result.cancelled) {
                this.setState({ image: result.uri });
            }

            console.log(result);
        } catch (E) {
            console.log(E);
        }
    };
}

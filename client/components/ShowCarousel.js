import React, {Component} from 'react';
import {
    Image,
    View,
    Text,
    TouchableOpacity,
} from 'react-native';

import styles from "../config/styles";

export default class ShowCarousel extends Component {

    render() {
        return (
            <View style={styles.imageContainer}>
                <Image style={styles.imageCarousel} source={{uri:this.props.image}}/>
                <TouchableOpacity
                    style={styles.deleteImageButton}
                    onPress={this.props.delete}>
                    <Text style={styles.deleteImageButtonText}>x</Text>
                </TouchableOpacity>
            </View>
        );
    }
}


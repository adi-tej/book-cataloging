import React, {Component} from 'react';
import {
    Image,
    View,
    Button, StyleSheet, Dimensions,
} from 'react-native';

export default class ShowCarousel extends Component {

    render() {
        return (
            <View>
                <Image style={styles.image} source={{uri:this.props.image}}/>
                <Button onPress={this.props.delete} title="Delete"/>
            </View>
        );
    }
}

const width = Dimensions.get('window').width;
const styles = StyleSheet.create({
    image:{
        backgroundColor: "lightgrey",
        borderColor: "lightgrey",
        borderWidth: 0.5,
        width: width/4,
        height: width/4,
        marginHorizontal: 8,
        marginVertical: 16,
        justifyContent:'center',
        alignItems:'center'
    },
})

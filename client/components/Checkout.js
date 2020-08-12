import React, {Component} from 'react';
import styles from "../config/styles";
import {
    View,
    Text,
    Image,
} from "react-native";
import images from "../config/images";

export default class Checkout extends Component {
    constructor(props) {
        super(props);
        this.book = this.props.book
        this.state = {
            modalVisible: this.props.modalVisible
        }
    }

    render() {
        return (
            <View style={styles.itemInfo}>
                <View style={styles.itemCoverView}>
                    <Image style={styles.itemCover} source={!this.book.cover ? images.noImage :
                            {uri:this.book.cover}}/>
                </View>
                <View style={styles.itemTitleView}>
                    <Text style={styles.itemTitle} numberOfLines={1}>{this.book.title}</Text>
                    <Text style={{color:"grey"}}>By {this.book.author}</Text>
                    <Text style={styles.itemPrice}>$ {this.book.price}</Text>
                </View>
            </View>);
    }
}

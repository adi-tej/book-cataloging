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
        // this.isbn = this.props.isbn;
        this.bookCover = "https://picsum.photos/id/237/200/300";
        this.title = "Shanghai";
        // this.genre = "fiction";
        this.author = "J.K. Rowling";
        this.price = 12;
        this.book = this.props.book
        // console.warn("info is: ", this.props.book)
        this.state = {
            modalVisible: this.props.modalVisible
        }
    }

    render() {
        return (
            // <View style={styles.checkoutPopup}>
            //     <View style={{paddingVertical:"10%",}}>
            <View style={styles.itemInfo}>
                <View style={styles.itemCoverView}>
                    <Image style={styles.itemCover} source={!this.book.cover ? images.noImage :
                            {uri:this.book.cover}}/>
                </View>
                <View style={styles.itemTitleView}>
                    <Text style={styles.itemTitle} numberOfLines={2}>{this.book.title}</Text>
                    <Text style={{color:"grey"}}>By {this.book.author}</Text>
                </View>
                <View style={styles.priceView}>
                    <Text style={{fontSize: 16}}>$ {this.book.price}</Text>
                </View>
            </View>);
    }
}

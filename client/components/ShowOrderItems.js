import React, {Component} from 'react';
import {
    Image,
    Text,
    View,
} from "react-native";
import styles from "../config/styles";

export default class ShowOrderItems extends Component {
    constructor(props) {
        super(props);
        this.isbn = this.props.isbn;
        this.title = this.props.title;
        this.bookCover = this.props.bookCover;
    }

    render() {
        if (this.isbn === "") {
            this.isbn = "No ISBN"
        }

        return (
            <View style={styles.itemContainer}>
                <View style={{flex: 1, flexDirection: "row"}}>
                    <View style={styles.itemCoverView}>
                        <Image style={styles.itemCover} source={{uri:this.bookCover}}/>
                    </View>
                    <View style={styles.itemTitleView}>
                        <Text style={styles.itemTitle} numberOfLines={2}>{this.title}</Text>
                        <Text style={{color:"grey"}}>ISBN: {this.isbn}</Text>
                    </View>
                    <View style={styles.priceView}>
                        <Text style={{fontSize: 16}}>$ {this.props.price}</Text>
                    </View>
                </View>
            </View>
        );
    }
}

import React, {Component} from 'react';
import {
    Image,
    Text,
    View,
} from "react-native";
import styles from "../config/styles";
import images from "../config/images";

export default class ShowOrderItems extends Component {
    constructor(props) {
        super(props);
        this.item = this.props.item;
        this.bookcover = this.item.cover;
        this.state = {
            isbn: this.item.isbn,
        }
        //
        // console.warn(this.props.item)
    }

    componentDidMount() {
        if (this.isbn === "") {
            this.setState({
                isbn: "No ISBN"
            })
        }
    }

    render() {

        return (
            <View style={styles.itemContainer}>
                <View style={{flex: 1, flexDirection: "row"}}>
                    <View style={styles.itemCoverView}>
                        <Image style={styles.itemCover} source={!this.bookcover ? images.noImage :
                            {uri:this.bookcover}}/>
                    </View>
                    <View style={styles.itemTitleView}>
                        <Text style={styles.itemTitle} numberOfLines={2}>{this.item.title}</Text>
                        <Text style={{color:"grey"}}>ISBN: {this.item.isbn}</Text>
                    </View>
                    <View style={styles.priceView}>
                        <Text style={{fontSize: 16}}>$ {this.item.price}</Text>
                    </View>
                </View>
            </View>
        );
    }
}

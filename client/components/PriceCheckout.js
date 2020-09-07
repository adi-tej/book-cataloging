import React, {Component} from 'react';
import styles from "../config/styles";
import {
    View,
    Text,
} from "react-native";


export default class PriceCheckout extends Component {
    constructor(props) {
        super(props);
        this.price = this.props.price
    }

    render() {
        return (
            <View>
                <View style={styles.textFormat}>
                    <Text style={{flex: 1}}>{(this.price.item_price + this.price.logistics_price).toFixed(2)}</Text>
                    <Text style={{flex: 1}}>{this.price.item_price}</Text>
                    <Text style={{flex: 1}}>{this.price.logistics_price}</Text>
                    <Text style={{flex: 1.3}}>{this.price.item_location}</Text>
                </View>

            </View>
        );
    }
}

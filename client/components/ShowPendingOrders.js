import React, {Component} from 'react';
import {
    View,
    Text,
    TouchableOpacity
} from "react-native";
import styles from "../config/styles";

//This class is to create a box of each order
export default class ShowPendingOrders extends Component {

    render() {
        return (
            <TouchableOpacity
                activityOpacity={0.5}
                style={styles.orderContainer} onPress={()=>alert("Successful click")}>
                <Text style={styles.orderNumberText}>Order #: {this.props.orderNumber}</Text>
                <View style={{flex: 1, flexDirection: "row"}}>
                    <Text style={styles.orderInfoText}>{this.props.timeout}</Text>
                    <Text style={styles.orderInfoText}>Total Price: {this.props.totalPrice}</Text>
                </View>
            </TouchableOpacity>

        );
    }
}

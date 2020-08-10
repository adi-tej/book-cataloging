import React, {Component} from 'react';
import {
    View,
    Text,
    TouchableOpacity
} from "react-native";
import styles from "../config/styles";

//This class is to create a box of each order
export default class ShowPendingOrders extends Component {
    //TODO: on press redirect to online order details page
    render() {
        return (
            <TouchableOpacity
                activityOpacity={0.5}
                style={styles.orderContainer}
                onPress={!this.props.confirmed ? ()=>
                    this.props.navigation.navigate('OrderDetails',
                        {order: this.props.order}) : null}>
                <Text style={styles.orderNumberText}>Order #: {this.props.order.order_id}</Text>
                <View style={{flex: 1, flexDirection: "row"}}>
                    <Text style={styles.orderInfoText}>Total price: ${this.props.order.total_price}</Text>
                    <Text style={styles.orderInfoText}>Item quantity: {this.props.order.items.length}</Text>
                </View>
            </TouchableOpacity>

        );
    }
}

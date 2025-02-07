import React, {Component} from 'react';
import {
    View,
    Text,
    TouchableOpacity
} from "react-native";
import styles from "../config/styles";

//This class is to create a box of each order
export default class ShowPendingOrders extends Component {
    constructor(props) {
        super(props);
        this.price = 0;
        this.state = {
            totalPrice: 0,
        }
    }

    componentDidMount() {
        const itemArray = this.props.order.items;
        itemArray.map((item) => {this.price = this.price + item.price })
        this.setState({totalPrice: this.price});
    }

    render() {
        return (
            <TouchableOpacity
            activityOpacity={0.5}
            style={styles.orderContainer}

            onPress={()=> this.props.navigation.navigate('OrderDetails', {
                    confirmed: this.props.confirmed,
                    order: this.props.order,
                    totalPrice: this.state.totalPrice,
                    navigation: this.props.navigation
            })}
            >
                <Text style={styles.orderNumberText}>Order #: {this.props.order.order_id}</Text>
                <View style={{flex: 1, flexDirection: "row"}}>
                    <Text style={styles.orderInfoText}>Total price: ${this.state.totalPrice}</Text>
                    <Text style={styles.orderInfoText}>Item quantity: {this.props.order.items.length}</Text>
                </View>
            </TouchableOpacity>

        );
    }
}

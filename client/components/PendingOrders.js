import React, {Component} from 'react';
import {ScrollView} from "react-native";
import styles from "../config/styles";
import ShowPendingOrders from "./ShowPendingOrders";

export default class PendingOrders extends Component {
    constructor(props) {
        super(props);
        this.updateOrderNumber = "";
        this.updateTimeout = 2;
        this.updateTotalPrice = 0;
        // these contents should be cleared and it should be an empty array
        this.state = {orderArray:[
                {orderNumber: 1, timeout: "01:36:00", totalPrice: 20},
                {orderNumber: 2, timeout: "02:36:00", totalPrice: 200},
                {orderNumber: 3, timeout: "01:35:01", totalPrice: 10.5},
                {orderNumber: 5, timeout: "02:36:00", totalPrice: 2},
                {orderNumber: 6, timeout: "02:36:00", totalPrice: 20.1},
                {orderNumber: 7, timeout: "02:36:00", totalPrice: 10.5},
                {orderNumber: 8, timeout: "02:36:00", totalPrice: 20},
                {orderNumber: 9, timeout: "02:36:05", totalPrice: 20},
                {orderNumber: 10, timeout: "02:36:20", totalPrice: 20},
                {orderNumber: 11, timeout: "02:16:00", totalPrice: 20},
            ]}
    }

    //This function is to remove a confirmed order
    removeComfirmedOrder = (index) => {
        const copyOrderArray = Object.assign([], this.state.orderArray);
        copyOrderArray.splice(index, 1)
        this.setState({
            orderArray: copyOrderArray
        })
    }

    //This function is to add a new order
    addNewOrder = () => {
        const copyOrderArray = Object.assign([], this.state.orderArray);
        copyOrderArray.push({
            orderNumber: this.updateOrderNumber,
            timeout: this.updateTimeout,
            totalPrice: this.updateTotalPrice
        })
        this.setState({
            orderArray: copyOrderArray
        })
    }

    render() {
        return (
            <ScrollView style={styles.container}>
                {
                    this.state.orderArray.map((order, index)=>{
                        return(
                            <ShowPendingOrders
                                key={order.orderNumber}
                                orderNumber={order.orderNumber}
                                timeout={order.timeout}
                                totalPrice={order.totalPrice}
                            />
                        )
                    })
                }
            </ScrollView>
        );
    }
}


import React, {Component} from 'react';
import {Alert, ScrollView} from "react-native";
import styles from "../config/styles";
import ShowPendingOrders from "./ShowPendingOrders";

import api  from "../config/axios";
export default class Orders extends Component {
    constructor(props) {
        super(props);
        this.updateOrderNumber = "";
        this.updateTimeout = 2;
        this.updateTotalPrice = 0;
        this.mode = this.props.mode;
        // these contents should be cleared and it should be an empty array
        this.state = {
            orderArray:[],
                // {orderNumber: 1, timeout: "01:36:00", totalPrice: 20},
                // {orderNumber: 2, timeout: "02:36:00", totalPrice: 200},
                // {orderNumber: 3, timeout: "01:35:01", totalPrice: 10.5},
                // {orderNumber: 5, timeout: "02:36:00", totalPrice: 2},
                // {orderNumber: 6, timeout: "02:36:00", totalPrice: 20.1},
                // {orderNumber: 7, timeout: "02:36:00", totalPrice: 10.5},
                // {orderNumber: 8, timeout: "02:36:00", totalPrice: 20},
                // {orderNumber: 9, timeout: "02:36:05", totalPrice: 20},
                // {orderNumber: 10, timeout: "02:36:20", totalPrice: 20},
                // {orderNumber: 11, timeout: "02:16:00", totalPrice: 20},
            }
    }
//TODO: API call to get orders data before rendering and set to state
    componentDidMount() {
        api.get('/order', {
                params: {
                    order_status: this.mode
                }
            })
                .then((response) => {
                    if (response.status === 200) {
                        console.warn(response.data.order_items)
                        this.setState({orderArray: response.data.order_items})
                    }

                })
                .catch(function (error) {
                   console.warn(error)
                })
    }

    // // //This function is to remove a confirmed order
    // removeComfirmedOrder = (index) => {
    //     const copyOrderArray = Object.assign([], this.state.orderArray);
    //     copyOrderArray.splice(index, 1)
    //     this.setState({
    //         orderArray: copyOrderArray
    //     })
    // }
    // //
    // // //This function is to add a new order
    // addNewOrder = () => {
    //     const copyOrderArray = Object.assign([], this.state.orderArray);
    //     copyOrderArray.push({
    //         orderNumber: this.updateOrderNumber,
    //         timeout: this.updateTimeout,
    //         totalPrice: this.updateTotalPrice
    //     })
    //     this.setState({
    //         orderArray: copyOrderArray
    //     })
    // }

    render() {
        return (
            <ScrollView style={styles.container}>
                {
                    this.state.orderArray.map((order, index)=>{
                        return(
                            <ShowPendingOrders
                                confirmed={this.mode !== "pending" }
                                key={order.order_id}
                                //TODO: need to update timer
                                navigation={this.props.navigation}
                                order={order}
                            />
                        )
                    })
                }
            </ScrollView>
        );
    }
}


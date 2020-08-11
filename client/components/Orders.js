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
        this.state = {
            orderArray:[],
            }
    }

//API call to get orders data before rendering and set to state
    componentDidMount() {
        api.get('/order', {
                params: {
                    status: this.mode
                }
            })
                .then((response) => {
                    if (response.status === 200) {
                        // console.warn(response.data)
                        this.setState({orderArray: response.data.orders})
                    }

                })
                .catch(function (error) {
                   console.warn(error)
                })
    }

    componentDidUpdate(prevProps, prevState, snapshot) {

        prevState = this.state
        setTimeout(
         () => {api.get('/order', {
                params: {
                    status: this.mode
                }
            })
                .then((response) => {
                    if (response.status === 200) {
                        // console.warn(response.data)
                        if (prevState.orderArray !== response.data.orders) {
                             this.setState({orderArray: response.data.orders})
                           }
                    }
                })
                .catch(function (error) {
                   console.warn(error)
                }) }
        , 10000)
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


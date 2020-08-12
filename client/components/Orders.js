import React, {Component} from 'react';
import {
    ScrollView,
    RefreshControl,
} from "react-native";
import styles from "../config/styles";
import ShowPendingOrders from "./ShowPendingOrders";

import api  from "../config/axios";

export default class Orders extends Component {
    constructor(props) {
        super(props);
        this.mode = this.props.mode;
        this.state = {
            orderArray:[],
            refreshing: false,
            }
    }

    componentDidMount() {
        api.get('/order', {
                params: {
                    status: this.mode
                }
            })
                .then((response) => {
                    if (response.status === 200) {
                        this.setState({orderArray: response.data.orders})
                    }

                })
                .catch(function (error) {
                   console.warn(error)
                })
    }

    refreshOrders = () => {
        this.setState({refreshing: true})
        setTimeout(
         () => {api.get('/order', {
                params: {
                    status: this.mode
                }
            })
                .then((response) => {
                    if (response.status === 200) {
                        // console.warn(response.data)
                        if (this.state.orderArray !== response.data.orders) {
                             this.setState({orderArray: response.data.orders})
                           }
                    }

                })
                .catch(function (error) {
                   console.warn(error)
                })
             this.setState({refreshing: false})
         }
        , 1000)
    }


    componentWillReceiveProps(nextProps) {
        if (nextProps.params !== undefined) {
            if (nextProps.params.refresh) {
                this.refreshOrders()
            }
        }
    }

    render() {
        return (
            <ScrollView
                style={styles.container}
                refreshControl={
                    <RefreshControl refreshing={this.state.refreshing}
                                    onRefresh={this.refreshOrders.bind(this)}
                    />
                }
            >
                {
                    this.state.orderArray.map((order, index)=>{
                        return(
                            <ShowPendingOrders
                                confirmed={this.mode !== "pending" }
                                key={order.order_id}
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


import React, {Component} from 'react';
import {
    SafeAreaView,
    Text,
    View,
    ScrollView,
    Alert,
    TouchableOpacity,
} from "react-native";
import {Header, Left, Body, Icon} from "native-base";
import styles from "../config/styles";
import ShowOrderItems from "./ShowOrderItems";

import api  from "../config/axios";

export default class OrderItemDetails extends Component {
    constructor(props) {
        super(props);
        this.orderNumber = this.props.route.params.order.order_id;
        this.itemsArray = this.props.route.params.order.items;
        this.totalPrice = this.props.route.params.totalPrice;
    }

    //TODO: call API to send confirm order to backend
    onConfirmPress = ()=> {
        api.post('/order/confirm', {
            order_id: this.orderNumber
          })
          .then((response) => {
            if (response.status === 200) {
                 Alert.alert("Successfully Confirm Order " + this.orderNumber)
                setTimeout(() => {
                    this.props.route.params.navigation.navigate("RootNavigator")},
                    1500
                )
            }
          })
          .catch(function (error) {
            console.warn(error);
            Alert.alert("Oops! This order can't be confirmed now. Please try it later.")
          });
    }


    render() {
        return (
            <SafeAreaView>
                <Header>
                    <Left>
                        <Icon onPress={() => this.props.navigation.goBack()} name='arrow-back' style={{marginHorizontal:'5%'}}/>
                    </Left>
                    <Body style={{marginRight:'30%'}}>
                        <Text
                            style={{fontSize:20,
                                fontWeight : 'bold',
                                marginBottom:"2%"}}>
                            Order#: {this.orderNumber}
                        </Text>
                    </Body>
                </Header>

                <View style={{marginTop:'2%'}}>
                    <ScrollView style={styles.scrollContainer}>
                        {
                            //TODO: update it to itemsArray and update the related info
                            this.itemsArray.map((info)=> {
                            return(
                                <ShowOrderItems
                                    key={info.item_id}
                                    item={info}
                                />
                            )
                        })}

                        {/*---------------setting for order summary------------------*/}
                        <Text style={[styles.summaryText,{color: "lightgrey"}]}>
                            ----------------------------------</Text>
                        <View style={styles.summaryContainer}>
                            <Text style={styles.summaryText}>
                            Item quantity: {this.itemsArray.length}</Text>
                            <Text style={styles.summaryText}>
                                Total Price: ${this.totalPrice}</Text>
                        </View>

                    </ScrollView>

                    <TouchableOpacity
                        activityOpacity={0.5}
                        style={[styles.searchButton,{marginVertical:"2%"}]}
                        onPress={this.onConfirmPress}
                        >
                        <Text style={styles.loginText}>Confirm Order</Text>
                    </TouchableOpacity>
                </View>
            </SafeAreaView>
        );
    }
}

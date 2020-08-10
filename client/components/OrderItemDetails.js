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
        console.warn("===order is:====", this.itemsArray);
        this.state = {
            itemArray:[
                {id:1, isbn: 1234567890123, bookCover: "https://picsum.photos/id/237/200/300", title: "Just Testing Books"},
                {id:2, isbn: 9781925538830, bookCover: "https://picsum.photos/seed/picsum/200/300", title: "Beyond Lemuria"},
                {id:3, isbn: "", bookCover: "https://picsum.photos/200/300/?blur", title: "Abstract Art, Artists, Ancient Egypt"},
                {id:4, isbn: 9781234567890, bookCover: "https://picsum.photos/id/870/200/300?grayscale&blur=2", title: "The Australian Native Bee Book"},
                {id:5, isbn: 9781234567890, bookCover: "https://picsum.photos/id/870/200/300?grayscale&blur=2", title: "The Australian Native Bee Book"},
                {id:6, isbn: "", bookCover: "https://picsum.photos/seed/picsum/200/300", title: "Beyond Lemuria"},
                {id:7, isbn: 9789460098123, bookCover: "https://picsum.photos/200/300/?blur", title: "Abstract Art, Artists, Ancient Egypt"},
            ]}
    }

    //TODO: call API to send confirm order to backend
    onConfirmPress = ()=> {
        Alert.alert("Successfully Confirm Order " + this.orderNumber)
        // api.post('/order/confirmation', {
        //      TODO: update the payload content
        //     firstName: 'Fred',
        //     lastName: 'Flintstone'
        //   })
        //   .then((response) => {
        //     if (response.status === 201) {
        //          Alert.alert("Successfully Confirm Order " + this.orderNumber)
        //     }
        //   })
        //   .catch(function (error) {
        //     console.warn(error);
        //     Alert.alert("Oops! This order can't be confirmed now. Please try it later.")
        //   });
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
                            this.state.itemArray.map((info)=> {
                            return(
                                <ShowOrderItems
                                    key={info.id}
                                    isbn={info.isbn}
                                    bookCover={info.bookCover}
                                    title={info.title}
                                />
                            )
                        })}
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

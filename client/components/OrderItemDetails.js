import React, {Component} from 'react';
import {
    SafeAreaView,
    Text,
    View,
    ScrollView,
    Alert,
    TouchableOpacity,
} from "react-native";
import styles from "../config/styles";
import ShowOrderItems from "./ShowOrderItems";

export default class OrderItemDetails extends Component {
    constructor(props) {
        super(props);
        this.orderNumber = this.props.route.params.orderNumber;
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
    }

    //TODO: get item details from backend

    render() {
        return (
            <SafeAreaView style={{marginTop:'10%'}}>
                <View>
                    <View style={{alignItems:"center"}}>
                        <Text
                            style={{fontSize:20,
                                fontWeight : 'bold',
                                marginBottom:"2%"}}>
                            Order#: {this.orderNumber}
                        </Text>
                    </View>

                    <ScrollView style={styles.scrollContainer}>
                        {
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

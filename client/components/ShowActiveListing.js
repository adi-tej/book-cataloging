import React, {Component} from 'react';
import {
    View,
    Text,
    Image,
    TouchableOpacity
} from "react-native";
import styles from "../config/styles";
import images from "../config/images";

export default class ShowActiveListing extends Component {

    constructor(props) {
        super(props);
    }
    render() {
        return (
            <TouchableOpacity
                activityOpacity={0.5}
                style={styles.itemContainer} onPress={() => this.props.navigation.navigate('BookCataloguing',{
                    edit:true,
                    book:this.props.book
            })}>
                <View style={{flex: 1, flexDirection: "row"}}>
                    <View style={styles.itemCoverView}>
                        <Image style={styles.itemCover} source={!this.props.book.cover?images.noImage:{uri:this.props.book.cover}}/>
                    </View>
                    <View style={styles.itemTitleView}>
                        <Text style={styles.itemTitle} numberOfLines={1}>{this.props.book.title}</Text>
                        <Text style={{color:"grey"}}>By {this.props.book.author}</Text>
                        <Text style={styles.itemPrice}>$ {this.props.book.price}</Text>
                    </View>
                </View>
            </TouchableOpacity>
        );
    }
}

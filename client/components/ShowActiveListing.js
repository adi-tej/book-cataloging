import React, {Component} from 'react';
import {
    View,
    Text,
    Image,
    TouchableOpacity
} from "react-native";
import styles from "../config/styles";
import images from "../config/images";
//This class is to create a box of each listing item
export default class ShowActiveListing extends Component {
    //TODO: redirect all props to edit listing
    render() {
        return (
            <TouchableOpacity
                activityOpacity={0.5}
                style={styles.itemContainer} onPress={() => this.props.navigation.navigate('BookCataloguing',{
                    edit:true,
                    book:this.props.book,
                    images:this.props.images
            })}>
                <View style={{flex: 1, flexDirection: "row"}}>
                    <View style={styles.itemCoverView}>
                        <Image style={styles.itemCover} source={!this.props.book.cover?images.noImage:{uri:this.props.book.cover}}/>
                    </View>
                    <View style={styles.itemTitleView}>
                        <Text style={styles.itemTitle} numberOfLines={2}>{this.props.book.title}</Text>
                        <Text style={{color:"grey"}}>By {this.props.book.author}</Text>
                        {/*<Text style={{color:"grey"}}>{this.props.genre}</Text>*/}
                    </View>
                    <View style={styles.priceView}>
                        <Text style={{fontSize: 16}}>$ {this.props.book.price}</Text>
                    </View>
                </View>
            </TouchableOpacity>
        );
    }
}

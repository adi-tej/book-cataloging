import React, {Component} from 'react';
import styles from "../config/styles";
import {
    View,
    Text,
    Image,
} from "react-native";


export default class Checkout extends Component {
    constructor(props) {
        super(props);
        // this.isbn = this.props.isbn;
        this.bookCover = "https://picsum.photos/id/237/200/300";
        this.title = "Shanghai";
        // this.genre = "fiction";
        this.author = "J.K. Rowling";
        this.price = 12;
        this.state = {
            modalVisible: this.props.modalVisible
        }
    }


    render() {
        return (
            // <View style={styles.checkoutPopup}>
            //     <View style={{paddingVertical:"10%",}}>
            <View style={styles.itemInfo}>
                <View style={styles.itemCoverView}>
                    <Image style={styles.itemCover} source={{uri:this.bookCover}}/>
                </View>
                <View style={styles.itemTitleView}>
                    <Text style={styles.itemTitle} numberOfLines={2}>{this.title}</Text>
                    <Text style={{color:"grey"}}>By {this.author}</Text>
                </View>
                <View style={styles.priceView}>
                    <Text style={{fontSize: 16}}>$ {this.price}</Text>
                </View>
            </View>);

                    {/*<TouchableOpacity*/}
                    {/*    activityOpacity={0.5}*/}
                    {/*    style={styles.removeButton}*/}
                    {/*    onPress={this.onButtonPress.bind(this)}>*/}
                    {/*    <Text style={styles.loginText}>Checkout item</Text>*/}
                    {/*</TouchableOpacity>*/}
            {/*    </View>*/}
            {/*</View>*/}
        // );
    }
}

import React, {Component} from 'react';
import {
    Image,
    Text,
    View,
} from "react-native";
import CheckBox from 'react-native-check-box';
import styles from "../config/styles";
import images from "../config/images";
import colors from "../config/colors";

export default class ShowOrderItems extends Component {
    constructor(props) {
        super(props);
        this.item = this.props.item;
        this.bookCover = this.item.cover;
        this.state = {
            isbn: this.item.isbn,
            isChecked: false,
        }
    }

    componentDidMount() {
        if (this.isbn === "") {
            this.setState({
                isbn: "No ISBN"
            })
        }
    }

    render() {

        return (
            <View style={[styles.itemContainer, {backgroundColor: 'transparent'}]}>
                <View style={{flex: 1, flexDirection: "row"}}>
                    <View style={styles.itemCoverView}>
                        <Image style={styles.itemCover} source={!this.bookCover ? images.noImage :
                            {uri:this.bookCover}}/>
                    </View>
                    <View style={styles.itemTitleView}>
                        <Text style={styles.itemTitle} numberOfLines={1}>{this.item.title}</Text>
                        <Text style={{color:"grey"}}>ISBN: {this.item.isbn}</Text>
                        <Text style={styles.itemPrice}>$ {this.item.price}</Text>
                    </View>
                    <CheckBox
                        style={{alignSelf: 'center'}}
                        onClick={() => {
                            this.setState({
                                isChecked: !this.state.isChecked
                            })
                        }}
                        checkBoxColor={colors.loginButton}
                        isChecked={this.state.isChecked}
                    />
                </View>
            </View>
        );
    }
}

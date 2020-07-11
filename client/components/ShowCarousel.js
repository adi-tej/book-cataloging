import React, {Component} from 'react';
import {
    Image,
    View,
    Text,
    TouchableOpacity,
} from 'react-native';
import { Modal } from 'react-native';
import ImageViewer from 'react-native-image-zoom-viewer';

import styles from "../config/styles";

export default class ShowCarousel extends Component {
    constructor(props) {
        super(props);
        this.image=[{url: this.props.image}]
        this.state={isImageShow: false}
    }

    openMax = () =>{this.setState({isImageShow: true})}

    render() {
        return (
            <View style={styles.imageContainer}>
                {/*------Implement showing the image and open the image------*/}
                <TouchableOpacity style={styles.imageCarousel} onPress={this.openMax.bind(this)}>
                    <Image style={styles.imageCarousel} source={{uri:this.props.image}}/>
                </TouchableOpacity>

                {this.state.isImageShow ?
                    <Modal visible={true} transparent={true}
                           opRequestClose={()=>{this.setState({isImageShow: false})}}>
                        <ImageViewer imageUrls={this.image}
                                     onClick={() => {
                                         this.setState({
                                             isImageShow: false
                                         })
                                     }}/>
                    </Modal> :
                    null
                }

                {/*------Implement delete image------*/}
                <TouchableOpacity
                    style={styles.deleteImageButton}
                    onPress={this.props.delete}>
                    <Text style={styles.deleteImageButtonText}>x</Text>
                </TouchableOpacity>
            </View>
        );
    }
}


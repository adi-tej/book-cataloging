import React, {  Component } from 'react';
import {
    Text,
    View,
    TextInput,
    Alert,
    TouchableOpacity,
    ScrollView,
    StyleSheet,
    SafeAreaView,
    Modal,
} from 'react-native';
import { KeyboardAwareScrollView } from 'react-native-keyboard-aware-scroll-view';
import {Header, Left, Body, Icon} from "native-base";
import RNPickerSelect from "react-native-picker-select";
import * as Permissions from "expo-permissions";
import * as ImagePicker from "expo-image-picker";
import ShowCarousel from "./ShowCarousel";
import styles from "../config/styles";
import api from "../config/axios";

export default class BookCataloguing extends Component{
    constructor(props) {
        super(props);
        this.state = {
            book:{
                id:"",
                title:"",
                isbn: "",
                genre: "",
                author: "",
                cover: "",
                page_count: 0,
                publisher:"",
                price: 0,
                condition:0,
                otherDetails: ""
            },
            imageArray:[],
            // imageId: this.state.imageArray.length,
            modalVisible:false,
            isbnError:false,
            priceError:false,
            initImage: null,
            edit:false
        };
        this.imageId = this.state.imageArray.length;
    }
//TODO: API call to get book data before rendering and set to state
    componentDidMount() {
        if(this.props.route && this.props.route.params){
            if(this.props.route.params.edit) {
                const book = this.props.route.params.book
                this.setState({
                    edit: true,
                    book: book,
                    imageArray: book.images
                })
            }
            if(this.props.route.params.isbn) {
                const isbn = this.props.route.params.isbn
                api.get('/book/autodescription/'+isbn)
                    .then(res => {
                        if(res.status === 200) {
                            const data = res.data
                            this.setState({
                                book:data,
                                imageArray: data.images
                            })
                        }else{
                            alert('Failed to fetch book details from ISBN '+isbn)
                            console.warn('Failed to fetch book auto description')
                        }
                    }).catch((error) => {
                        console.warn(error.message)
                })
            }
        }

    }
    requestApi = (url, errMsg) => {
        let reqData = new FormData();
        for ( let key in this.state.book ) {
            reqData.append(key, JSON.stringify(this.state.book[key]));
        }
        api.put(url, reqData,{
            headers:{
                'Content-Type': null
            }
        })
            .then(res => {
                if(res.status === 200) {
                    this.props.navigation.navigate('RootNavigator')
                }else{
                    alert(errMsg)
                }
            }).catch((error)=>{
            console.warn(error.message);
        });
    }
    onButtonPress() {
        if (this.state.book.title === "" || this.state.book.condition === "" || this.state.book.price === 0) {
            Alert.alert("Warning:",
                "You have to fill out Title, Condition and Price")
        } else{
            //TODO: API call to submit and redirect to RootNavigator
            if(this.state.edit){
                //TODO: API call to edit the listing
                this.requestApi(`/book/`+this.state.book.id, "Failed to edit book")
            }else{
                //TODO: API call to create the listing
                this.requestApi(`/book/list`, "Failed to list on ebay")
            }
        }
    }

    onRemoveButtonPress(){
        //popup to confirm remove listing
        this.setState({modalVisible:true})
    }

    onConfirmRemovePress = () =>{
        this.setState({modalVisible:false})
        //TODO: API call to remove listing
        api.delete(`/book/`+this.state.book.id)
            .then(res => {
                if(res.status === 200) {
                    this.props.navigation.navigate('RootNavigator')
                }else{
                    alert('Failed to remove item')
                }
            }).catch((error)=>{
            console.warn(error.message);
        });
    }

    deleteImage = (index) =>{
        const copyImageArray = Object.assign([], this.state.imageArray);
        copyImageArray.splice(index, 1)
        this.setState({
            imageArray: copyImageArray
        })
    };

    validISBN = () => {
        if ((this.state.book.isbn.length !== 10) && (this.state.book.isbn.length !== 13) && (this.state.book.isbn !== "")){
            this.setState({isbnError: true})
        } else{
            this.setState({isbnError: false})
        }
    }

    validPrice = () => {
        const re = /^\d+\.?\d*$/;
        if (!re.test(this.state.book.price)) {
            this.setState({priceError: true})
        } else {
            this.setState({priceError: false})
        }
    }

    takePicture = async() => {
        await Permissions.askAsync(Permissions.CAMERA);
        const {cancelled, uri} = await ImagePicker.launchCameraAsync({
            allowsEditing: true,
            aspect: [1,1],
            quality: 0.5
        });
        if (!cancelled) {
            this.setState({initImage: uri});
            //add this image to imageArray
            // while (this.imageId + 1  in this.state.imageArray.id){
            //     this.imageId = this.imageId + 1;
            // }
            let imgIds = []
            this.state.imageArray.forEach((img) => {
                imgIds.push(img.id)
            })
            while (imgIds.includes(this.imageId)){
                this.imageId = this.imageId + 1;
            }

            const copyImageArray = Object.assign([], this.state.imageArray);
            copyImageArray.push({
                id: this.imageId,
                uri: this.state.initImage //update "image" to "uri"
            })
            this.setState({
                imageArray: copyImageArray
            })
        }
    };

    //TODO: All fields regex check
    render() {
        return ( //show all details of the book
            <SafeAreaView style={{flex:1}}>
                <Header>
                    <Left>
                        <Icon onPress={() => this.props.navigation.goBack()} name='arrow-back' style={{marginHorizontal:'5%'}}/>
                    </Left>
                    <Body style={{marginRight:'30%'}}><Text style={styles.listingTitle}>
                        {this.state.edit ? 'Edit book':'List a book'} </Text></Body>
                </Header>
                <KeyboardAwareScrollView behavior="padding" style={[styles.container,{marginTop:'5%'}]}>

                {/*Create an Image Carousel*/}
                <View>
                    <ScrollView horizontal={true} style={{flexDirection: "row"}}>
                        {
                            this.state.imageArray.map((image, index)=>{
                                return(
                                    <ShowCarousel
                                        image={image.uri}
                                        key={image.id}
                                        delete={this.deleteImage.bind(this, index)}
                                    />
                                )
                            })
                        }
                        {/*{console.warn("imageArray:", this.state.imageArray)}*/}
                        {this.state.imageArray.length < 10 ?
                            <TouchableOpacity
                                activityOpacity={0.5}
                                style={styles.imageContainer}
                                onPress={this.takePicture.bind(this)}>
                                <Text style={styles.loginText}>+</Text>
                            </TouchableOpacity> : null
                        }
                    </ScrollView>
                    <Text style={[styles.requiredText, {fontSize: 14, marginBottom:"2%"}]}>* Max number of images: 10</Text>
                </View>

                {/*Create other information View*/}
                <View style={{flex: 1, flexDirection: "row"}}>
                    <Text style={styles.listingTitle}>Title: </Text>
                    <Text style={styles.requiredText}>*</Text>
                </View>
                <TextInput
                    underlineColorAndroid={"transparent"}
                    style={styles.textInput}
                    clearButtonMode={"while-editing"}
                    value={this.state.book.title}
                    onChangeText={(title) => this.setState({book:{...this.state.book,title:title}})}
                />

                <Text style={styles.listingTitle}>ISBN: </Text>
                <TextInput
                    underlineColorAndroid={"transparent"}
                    style={styles.textInput}
                    keyboardType="number-pad"
                    clearButtonMode={"while-editing"}
                    maxLength={13}
                    onBlur={this.validISBN.bind(this)}
                    value={this.state.book.isbn}
                    onChangeText={(isbn) => this.setState({book:{...this.state.book,isbn:isbn}})}
                />
                    {this.state.isbnError?
                        <Text style={{color:'red'}}>Please enter 10 or 13 digits</Text>
                        : null
                    }

                <Text style={styles.listingTitle}>Genre: </Text>
                <TextInput
                    underlineColorAndroid={"transparent"}
                    style={styles.textInput}
                    clearButtonMode={"while-editing"}
                    value={this.state.book.genre}
                    onChangeText={(genre) => this.setState({book:{...this.state.book,genre:genre}})}
                />

                <Text style={styles.listingTitle}>Author: </Text>
                <TextInput
                    underlineColorAndroid={"transparent"}
                    style={styles.textInput}
                    clearButtonMode={"while-editing"}
                    value={this.state.book.author}
                    onChangeText={(author) => this.setState({book:{...this.state.book,author:author}})}
                />

                <Text style={styles.listingTitle}>Page: </Text>
                <TextInput
                    underlineColorAndroid={"transparent"}
                    style={styles.textInput}
                    clearButtonMode={"while-editing"}
                    keyboardType="number-pad"
                    value={this.state.book.page_count?this.state.book.page_count:0}
                    onChangeText={(page) => this.setState({book:{...this.state.book,page_count:page}})}
                />

                <Text style={styles.listingTitle}>Publisher: </Text>
                <TextInput
                    underlineColorAndroid={"transparent"}
                    clearButtonMode={"while-editing"}
                    style={styles.textInput}
                    value={this.state.book.publisher}
                    onChangeText={(publisher) => this.setState({book:{...this.state.book,publisher:publisher}})}
                />

                <View style={{flex: 1, flexDirection: "row"}}>
                    <Text style={styles.listingTitle}>Price: </Text>
                    <Text style={styles.requiredText}>*</Text>
                </View>
                <TextInput
                    underlineColorAndroid={"transparent"}
                    style={styles.textInput}
                    clearButtonMode={"while-editing"}
                    onBlur={this.validPrice.bind(this)}
                    value={this.state.book.price?this.state.book.price:0}
                    onChangeText={(price) => this.setState({book:{...this.state.book,price:price.trim()}})}
                />
                    {this.state.priceError?
                        <Text style={{color:'red'}}>Please enter a valid price</Text>
                        : null
                    }

                <View style={{flex: 1, flexDirection: "row"}}>
                    <Text style={styles.listingTitle}>Condition: </Text>
                    <Text style={styles.requiredText}>*</Text>
                </View>
                <RNPickerSelect
                    onValueChange={(condition) => this.setState({book:{...this.state.book,condition:condition}})}
                    style={{
                        ...pickerSelectStyles,
                        // iconContainer: {
                        // top: 20,
                        // right: 10,},
                    }}
                    items={[
                        { label: 'New', value: 1000 },
                        { label: 'Like new', value: 2750 },
                        { label: 'Used', value: 3000 },
                        { label: 'Very good', value: 4000 },
                        { label: 'Good', value: 5000 },
                        { label: 'Acceptable', value: 6000 },
                    ]}
                    placeholder={{label: "Select a condition..."}}
                    useNativeAndroidPickerStyle={false}
                    textInputProps={{ underlineColor: 'transparent' }}
                    // Icon={() => {
                    //     return <Icon name="arrow-down" size={16} color="lightgrey" />;
                    // }}

                />

                <Text style={styles.listingTitle}>Other Details: </Text>
                <TextInput
                    underlineColorAndroid={"transparent"}
                    style={styles.textInput}
                    clearButtonMode={"while-editing"}
                    multiline={true}
                    onChangeText={(otherDetails) => this.setState({book:{otherDetails:otherDetails}})}
                />

                <View style={styles.buttonView}>
                <TouchableOpacity
                    activityOpacity={0.5}
                    style={styles.removeButton}
                    onPress={this.onButtonPress.bind(this)}>
                    <Text style={styles.loginText}>{
                       this.state.edit ? 'Update' : 'List on eBay'
                    }</Text>
                </TouchableOpacity>
                {
                    this.state.edit ?
                        <TouchableOpacity
                            activityOpacity={0.5}
                            style={styles.removeButton}
                            onPress={this.onRemoveButtonPress.bind(this)}>
                            <Text style={styles.loginText}>Remove Item</Text>
                        </TouchableOpacity> : null
                }
                </View>

                {/*------------------------setting remove-item modal---------------------------*/}
                <Modal
                    transparent={true}
                    visible={this.state.modalVisible}
                >
                    <View style={styles.modalView}>
                        <View style={styles.noIsbnPopup}>
                            <View style={{alignItems:"center", justifyItems:"center"}}>
                                <Text style={[styles.warningText, {paddingHorizontal: "5%",}]}>
                                    Warning: You will remove this item from eBay and delete it from database.
                                </Text>
                                <Text style={[styles.warningText, {
                                    fontSize: 20,
                                    fontWeight:"bold",
                                    padding: "2%",
                                    color: "black"}]}>
                                    Do you confirm removal?
                                </Text>
                                <View style={styles.buttonView}>
                                    <TouchableOpacity
                                        activityOpacity={0.5}
                                        style={[styles.removeButton, {width:"30%"}]}
                                        onPress={this.onConfirmRemovePress}>
                                        <Text style={styles.loginText}>Yes</Text>
                                    </TouchableOpacity>
                                    <TouchableOpacity
                                        activityOpacity={0.5}
                                        style={[styles.removeButton, {width:"30%", backgroundColor: "lightgrey"}]}
                                        onPress={()=>this.setState({modalVisible: false})}>
                                        <Text style={styles.loginText}>No</Text>
                                    </TouchableOpacity>
                                </View>
                            </View>
                        </View>
                    </View>
                </Modal>
                </KeyboardAwareScrollView>
            </SafeAreaView>
        )
    }
}

const pickerSelectStyles = StyleSheet.create({
    inputIOS: {
        fontSize: 16,
        paddingVertical: "2%",
        borderWidth: 1,
        borderColor: 'black',
        color: 'black',
        paddingRight: 30, // to ensure the text is never behind the icon
        padding : '2%',
        marginVertical : '2%'
    },
    inputAndroid: {
        fontSize: 16,
        paddingVertical: "2%",
        borderWidth: 1,
        borderColor: 'black',
        color: 'black',
        paddingRight: 30, // to ensure the text is never behind the icon
        padding : '2%',
        marginVertical : '2%'
    },
});

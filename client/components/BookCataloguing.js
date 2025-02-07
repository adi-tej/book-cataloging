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
    Modal, Dimensions,
} from 'react-native';
import { KeyboardAwareScrollView } from 'react-native-keyboard-aware-scroll-view';
import {Header, Left, Body, Icon} from "native-base";
import RNPickerSelect from "react-native-picker-select";
import * as Permissions from "expo-permissions";
import * as ImagePicker from "expo-image-picker";
import ShowCarousel from "./ShowCarousel";
import styles from "../config/styles";
import api from "../config/axios";
import PriceCheckout from "./PriceCheckout";

const width = Dimensions.get('window').width;

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
                edition: 0,
                cover: "",
                page_count: 0,
                weight: 0,
                publisher:"",
                price: 0,
                condition:0,
                description: ""
            },
            imageArray:[],
            checkPriceArray:[],
            priceModalVisible:false,
            modalVisible:false,
            isbnError:false,
            priceError:false,
            initImage: null,
            edit:false
        };
        this.imageId = this.state.imageArray.length + 1;
    }

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
                                book:data
                            })
                            if(data.images){
                                this.setState({
                                    imageArray: data.images
                                })
                            }
                        }else{
                            alert('Failed to fetch book details from ISBN '+isbn)
                            console.log('Failed to fetch book auto description')
                        }
                    }).catch((error) => {
                        console.log(error.message)
                })
            }
        }

    }
    getFormData = () => {
        let reqData = new FormData();
        this.state.book.images = this.state.imageArray
        for ( let key in this.state.book ) {
            if(key === 'images') {
                reqData.append(key, JSON.stringify(this.state.book[key]));
            }else{
                reqData.append(key, this.state.book[key]);
            }
        }
        this.state.imageArray.forEach((image, i) => {
            reqData.append("image"+image.id.toString(), {
                uri: image.uri,
                type: "image/jpeg",
                name: image.id.toString()
            });
        });
        return reqData

    }
    onButtonPress() {

        if (this.state.book.title === "" || this.state.book.condition === "" ||
            this.state.book.price === "" || this.state.book.description === "" ||
            this.state.imageArray.length === 0) {
            Alert.alert("Warning:",
                "You have to fill out Title, Condition, Price, Description and add at-least one image")
        } else{
            if(this.state.edit){
                let reqData = this.getFormData()
                api.put(`/book/`+this.state.book.id, reqData,{
                    headers:{
                        'Content-Type': null
                    }
                })
                    .then(res => {
                        if(res.status === 200) {
                            this.props.navigation.navigate('Active Listing',{refresh:true})
                        }else{
                            alert("Failed to edit book")
                        }
                    }).catch((error)=>{
                    console.log(error.message);
                });
            }else{
                let reqData = this.getFormData()
                api.post(`/book/list`, reqData,{
                    headers:{
                        'Content-Type': null
                    }
                })
                    .then(res => {
                        if(res.status === 200) {
                            console.log(res.data)
                            this.props.navigation.navigate('Active Listing',{refresh:true})
                        }else{
                            alert("Failed to list on ebay")
                        }
                    }).catch((error)=>{
                    console.log(error.message);
                });
            }
        }
    }

    onRemoveButtonPress(){
        //popup to confirm remove listing
        this.setState({modalVisible:true})
    }

    onConfirmRemovePress = () =>{
        this.setState({modalVisible:false})
        api.delete(`/book/`+this.state.book.id)
            .then(res => {
                if(res.status === 200) {
                    this.props.navigation.navigate('Active Listing',{refresh:true})
                }else{
                    alert('Failed to remove item')
                    console.log('Failed to remove item')
                }
            }).catch((error)=>{
            console.log(error.message);
        });
    }

    onCheckPricePress = () => {

        const isbn = this.state.book.isbn
        api.get('/book/autopricing/'+isbn)
                    .then(res => {
                        if(res.status === 200) {
                            const data = res.data
                            if(data.prices_array){
                                this.setState({
                                    checkPriceArray: data.prices_array
                                })
                            }
                            this.setState({priceModalVisible: true})
                            // console.warn(res.data.prices_array)

                        }else{
                            Alert.alert('Failed to fetch book prices from eBay')
                        }
                    }).catch((error) => {
                        Alert.alert('Failed to fetch book prices from eBay')
                        console.warn(error.message)
                })
    }

    deleteImage = (index) =>{
        if(index === 0){
            if(this.state.book.cover !== ''){
                this.state.book.cover = ''
            }
        }
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
                        {this.state.imageArray.length < 10 ?
                            <TouchableOpacity
                                activityOpacity={0.5}
                                style={styles.imageContainer}
                                onPress={this.takePicture.bind(this)}>
                                <Text style={styles.loginText}>+</Text>
                            </TouchableOpacity> : null
                        }
                    </ScrollView>
                    <Text style={[styles.requiredText, {fontSize: 14, marginBottom:"2%"}]}>* You must upload at least 1 and up to 10 images</Text>
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
                    multiline={true}
                    onChangeText={(title) => this.setState({book:{...this.state.book,title:title}})}
                />
                    {this.state.book.title.length>35 ?
                         <Text style={{color:'red', marginBottom:'2%'}}> Exceeds by {this.state.book.title.length-35} chars...</Text>
                        :null
                    }

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
                    value={this.state.book.page_count?this.state.book.page_count.toString():null}
                    onChangeText={(page) => this.setState({book:{...this.state.book,page_count:page}})}
                />

                <Text style={styles.listingTitle}>Estimated Weight(kg): </Text>
                <TextInput
                    underlineColorAndroid={"transparent"}
                    style={styles.textInput}
                    clearButtonMode={"while-editing"}
                    keyboardType="number-pad"
                    value={this.state.book.weight?this.state.book.weight.toString():null}
                    onChangeText={(weight) => this.setState({book:{...this.state.book,weight:weight}})}
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
                    <Text style={styles.listingTitle}>Price (AU$): </Text>
                    <Text style={styles.requiredText}>*</Text>
                </View>
                <View style={{flex: 1, flexDirection: "row"}}>
                    <TextInput
                    underlineColorAndroid={"transparent"}
                    style={[styles.textInput, {width: '60%'}]}
                    clearButtonMode={"while-editing"}
                    onBlur={this.validPrice.bind(this)}
                    value={this.state.book.price?this.state.book.price.toString():null}
                    onChangeText={(price) => this.setState({book:{...this.state.book,price:price.trim()}})}
                    />
                    <TouchableOpacity
                    activityOpacity={0.5}
                    style={[styles.loginButton, {marginHorizontal: '3%'}]}
                    onPress={this.onCheckPricePress.bind(this)}>
                        <Text style={{color: 'white', fontSize: 18}}>Check Price</Text>
                    </TouchableOpacity>
                </View>
                    {this.state.priceError?
                        <Text style={{color:'red'}}>Please enter a valid price</Text>
                        : null
                    }
                <View style={{flex: 1, flexDirection: "row"}}>
                    <Text style={styles.listingTitle}>Condition: </Text>
                    <Text style={styles.requiredText}>*</Text>
                </View>
                <RNPickerSelect
                    value={this.state.book.condition}
                    onValueChange={(condition) => this.setState({book:{...this.state.book,condition:condition}})}
                    style={{
                        ...pickerSelectStyles,
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

                />

                <View style={{flex: 1, flexDirection: "row"}}>
                    <Text style={styles.listingTitle}>Description: </Text>
                    <Text style={styles.requiredText}>*</Text>
                </View>
                <TextInput
                    underlineColorAndroid={"transparent"}
                    style={styles.textInput}
                    clearButtonMode={"while-editing"}
                    multiline={true}
                    value={this.state.book.description}
                    onChangeText={(description) => this.setState({book:{...this.state.book,description:description}})}
                />
                {this.state.book.description.length>800 ?
                         <Text style={{color:'red', marginBottom:'2%'}}> Exceeds by {this.state.book.description.length-800} chars...</Text>
                        :null
                    }

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

                {/*--------------------------------------check price modal------------------------------------------*/}
                <Modal
                    transparent={true}
                    visible={this.state.priceModalVisible}
                >
                    <View style={{backgroundColor:"#000000aa", flex: 1}}>
                        <View style={[styles.checkoutPopup, {height: '80%'}]}>

                            <TouchableOpacity
                                style={styles.closeButton}
                                onPress={() => this.setState({priceModalVisible: false})}
                            >
                                <Text style={{ fontSize: 18, color: 'lightgrey'}}> X </Text>
                            </TouchableOpacity>

                            <View style={styles.setPrice}>
                                <Text style={{fontWeight: "bold", fontSize: 18,}}> Set Price (AU$): </Text>
                                <TextInput
                                    underlineColorAndroid={"transparent"}
                                    style={[styles.textInput, {width: '30%', fontSize: 18}]}
                                    clearButtonMode={"while-editing"}
                                    onBlur={this.validPrice.bind(this)}
                                    value={this.state.book.price?this.state.book.price.toString():null}
                                    onChangeText={(price) => this.setState({book:{...this.state.book,price:price.trim()}})}
                                />
                                <TouchableOpacity
                                    activityOpacity={0.5}
                                    style={[styles.loginButton, {marginHorizontal: '3%'}]}
                                    onPress={() => this.setState({priceModalVisible: false})}>
                                    <Text style={{color: 'white', fontSize: 18}}> Go </Text>
                                </TouchableOpacity>
                            </View>

                            <Text style={{
                                color: "lightgrey",
                                textAlign: "center",
                                marginTop: "2%",
                            }}>{"-".repeat(width*0.14)}</Text>
                            <Text style={styles.priceModalTitle}>Recommended Price (AU$)</Text>

                            {/*====================================================*/}
                            <View style={styles.headerFormat}>
                                <Text style={{flex: 1, fontWeight: "bold"}}>Total price</Text>
                                <Text style={{flex: 1, fontWeight: "bold"}}>Item price</Text>
                                <Text style={{flex: 1, fontWeight: "bold"}}>Postage</Text>
                                <Text style={{flex: 1.3, fontWeight: "bold"}}>Item location</Text>
                            </View>
                            <ScrollView style={{marginBottom: "5%"}}>
                                {
                                    this.state.checkPriceArray.map((price, index)=>{
                                        return(
                                            <PriceCheckout
                                                price={price}
                                                key={index}/>)
                                    })
                                }
                                <Text style={styles.resourceText}>
                                    (Data Resource: eBay platform)</Text>
                            </ScrollView>

                            {/*==============================================================*/}

                        </View>
                    </View>
                </Modal>

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

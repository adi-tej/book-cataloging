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
        this.imageId = 0;
        this.state = {
            book:{
                id:"",
                title:"",
                isbn: "",
                genre: "",
                author: "",
                pages: 0,
                publisher:"",
                price: 0,
                condition:"",
                otherDetails: ""
            },
            imageArray:[],
            modalVisible:false,
            isbnError:false,
            initImage: null,
            edit:false
        }
    }
//TODO: API call to get book data before rendering and set to state
    componentDidMount() {
        if(this.props.route && this.props.route.params){
            if(this.props.route.params.edit) {
                const book = this.props.route.params.book
                this.setState({
                    edit: true,
                    book: book
                })
            }
            if(this.props.route.params.isbn) {
                const isbn = this.props.route.params.isbn
                api.get('/book/autodescription/'+isbn)
                    .then(res => {
                        if(res.status === 200) {
                            const data = res.data
                            const copyImageArray = Object.assign([], this.state.imageArray);
                            copyImageArray.push({
                                id: this.state.imageId,
                                image: data.cover
                            })
                            this.setState({
                                book:data,
                                imageArray: copyImageArray
                            })
                        }else{
                            console.warn('Failed to fetch book auto description')
                        }
                    }).catch((error) => {
                        console.warn('Failed to fetch book auto description')
                })
            }
        }
        // api.get(`/user/home`)
        //     .then(res => {
        //         console.warn(res)
        //         const data = res.data;
        //         this.setState({ title: data.title });
        //     }).catch((error)=>{
        //         console.log("Api call error");
        //         console.warn(error.message);
        // });

    }

    onButtonPress() {
        if (this.state.title === "" || this.state.condition === "" || this.state.price === 0) {
            Alert.alert("Warning:",
                "You have to fill out Title, Condition and Price")
        } else{
            //TODO: API call to submit and redirect to RootNavigator
            Alert.alert("BookCataloguing book: " + this.state.title)
            if(this.state.edit){
                //TODO: API call to edit the listing
                api.put(`/book/`+this.state.book.id)
                    .then(res => {
                        console.warn(res)
                        const data = res.data;
                        // this.setState({ title: data.title });
                        this.props.navigation.navigate('RootNavigator')
                    }).catch((error)=>{
                        console.warn(error.message);
                });
            }else{
                //TODO: API call to create the listing
                api.put(`/book/list`,this.state.book)
                    .then(res => {
                        console.warn(res)
                        const data = res.data;
                        // this.setState({ title: data.title });
                        this.props.navigation.navigate('RootNavigator')
                    }).catch((error)=>{
                    console.warn(error.message);
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
        //TODO: API call to remove listing
        api.delete(`/book/`+this.state.book.id)
            .then(res => {
                console.warn(res)
                const data = res.data;
                // this.setState({ title: data.title });
                this.props.navigation.navigate('RootNavigator')
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
        if ((this.state.isbn.length !== 10) && (this.state.isbn.length !== 13) && (this.state.isbn !== "")){
            this.setState({isbnError: true})
        } else{
            this.setState({isbnError: false})
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
            this.imageId = this.imageId + 1;
            const copyImageArray = Object.assign([], this.state.imageArray);
            copyImageArray.push({
                id: this.imageId,
                image: this.state.initImage
            })
            this.setState({
                imageArray: copyImageArray
            })
        }
    };
    //TODO: All fields regex check
    render() {
        return (
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
                                        image={image.image}
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
                    onChangeText={(title) => this.setState({title})}
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
                    onChangeText={(isbn) => this.setState({isbn})}
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
                    onChangeText={(genre) => this.setState({genre})}
                />

                <Text style={styles.listingTitle}>Author: </Text>
                <TextInput
                    underlineColorAndroid={"transparent"}
                    style={styles.textInput}
                    clearButtonMode={"while-editing"}
                    value={this.state.book.author}
                    onChangeText={(author) => this.setState({author})}
                />

                <Text style={styles.listingTitle}>Page: </Text>
                <TextInput
                    underlineColorAndroid={"transparent"}
                    style={styles.textInput}
                    clearButtonMode={"while-editing"}
                    keyboardType="number-pad"
                    value={this.state.book.pages?this.state.book.pages.toString():0}
                    onChangeText={(page) => this.setState({page})}
                />

                <Text style={styles.listingTitle}>Publisher: </Text>
                <TextInput
                    underlineColorAndroid={"transparent"}
                    clearButtonMode={"while-editing"}
                    style={styles.textInput}
                    value={this.state.book.publisher}
                    onChangeText={(publisher) => this.setState({publisher})}
                />

                <View style={{flex: 1, flexDirection: "row"}}>
                    <Text style={styles.listingTitle}>Price: </Text>
                    <Text style={styles.requiredText}>*</Text>
                </View>
                <TextInput
                    underlineColorAndroid={"transparent"}
                    style={styles.textInput}
                    clearButtonMode={"while-editing"}
                    keyboardType="number-pad"
                    value={this.state.book.price?this.state.book.price.toString():0}
                    onChangeText={(price) => this.setState({price})}
                />


                <View style={{flex: 1, flexDirection: "row"}}>
                    <Text style={styles.listingTitle}>Condition: </Text>
                    <Text style={styles.requiredText}>*</Text>
                </View>
                <RNPickerSelect
                    onValueChange={(condition) => this.setState({condition})}
                    style={{
                        ...pickerSelectStyles,
                        // iconContainer: {
                        // top: 20,
                        // right: 10,},
                    }}
                    items={[
                        { label: 'Brand new', value: 'Brand new' },
                        { label: 'Like new', value: 'Like new' },
                        { label: 'Very good', value: 'Very good' },
                        { label: 'Good', value: 'Good' },
                        { label: 'Acceptable', value: 'Acceptable' },
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
                    onChangeText={(otherDetails) => this.setState({otherDetails})}
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

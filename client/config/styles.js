import {StyleSheet} from "react-native";
import colors from "./colors";


import { Dimensions } from 'react-native';
import React from "react";

const width = Dimensions.get('window').width;
const height = Dimensions.get('window').height;


const styles = StyleSheet.create({
    /**
     * Login
     */
    container : {
        flexDirection: 'column',
        flex : 1,
        margin : '5%'
    },
    header : {
      height : '10%'
    },
    image:{
        marginTop : '30%',
        marginBottom : '40%',
        alignSelf : 'center',
        height:width*0.5,
        width:width*0.5,
    },
    textInput : {
        width : '100%',
        borderColor: 'black',
        paddingHorizontal : '2%',
        borderWidth: 1,
        fontSize : 16,
        marginVertical : '2%',
        padding : '2%',
    },
    loginButton : {
        marginVertical : '2%',
        padding : '3%',
        color: 'white',
        backgroundColor: colors.loginButton,
        alignItems : 'center'
    },
    loginText : {
        color : 'white',
        fontWeight : 'bold',
        fontSize : 20
    },
    resetAccountButton : {
        marginVertical : '2%',
        alignSelf: 'center',
        color : colors.loginButton,
        fontSize : 18
    },
    /**
     * Barcode Scanner
     */
    cameraOption : {
        height:'5%',
        justifyContent:'center',
        alignItems: 'center',
        backgroundColor:'rgba(0,0,0,0.5)',
        borderRadius:5,
        marginTop : '7%'
    },
    contextMenuText : {
        backgroundColor: colors.drawer,
        fontSize: 24,
        color: 'white',
        paddingVertical:'7%',
        width:'100%',
        textAlign:'center'
    },
    checkoutButton:{
        flex:1,
        width:'40%',
        position:'absolute',
        justifyContent:'center',
        backgroundColor:colors.drawer,
        alignItems:'center',
        padding:'8%',
        bottom:'10%',
        right:'5%',
        borderRadius:30
    },
    contextMenuContainer:{
        flex:1,
        backgroundColor:'transparent',
        marginTop:'10%',
        marginRight:'10%',
        width:'35%',
        justifyContent:'center'
    },
    /**
     * Camera tab navigator
     */
    cameraComponent:{
        flex: 1,
        flexDirection: 'column',
        justifyContent: 'flex-end',
    },
    barcodeCameraComponent:{
        flex: 1,
        backgroundColor: 'transparent',
        flexDirection:'row'
    },
    cameraScanTab:{
        justifyContent:'center'
    },
    cameraScanTabLabel:{
        backgroundColor:'transparent',
        fontSize : 20,
        paddingVertical :'5%'
    },
    cameraScanTabNavigator:{
        backgroundColor:'transparent',
        height:'10%',
        position: 'absolute',
        left: 0,
        bottom: 0,
        right: 0,
        borderTopColor:'transparent'
    },
    /**
     * Book Cataloging
     * Edit Listing
     * Image carousal
     */
    imageContainer:{
        flex: 1,
        backgroundColor: "lightgrey",
        width: width/4,
        height: width/4,
        marginBottom: width/30,
        marginRight: width/100,
        justifyContent:'center',
        alignItems:'center',
    },
    imageCarousel:{
        flex: 1,
        width: width/4,
        height: width/4,
        justifyContent:'center',
        alignItems:'center',
        position:'absolute',
        left:0,
        right: 0,
        top: 0,
        bottom:0
    },
    listingTitle: {
        fontSize: 16,
        color: "black",
        fontWeight: "bold",
    },
    deleteImageButton:{
        height: width/20,
        width: width/20,  //The Width must be the same as the height
        borderRadius:width/10, //Then Make the Border Radius twice the size of width or Height
        borderColor: 'white',
        position: "absolute",
        right: 5,
        top: 5,
        justifyContent:'center',
        alignItems: 'center',
        backgroundColor:'rgba(255,0,0,0.5)',
    },
    deleteImageButtonText: {
        fontSize: 10,
        fontWeight: "bold",
        color: 'white',
        textAlign:'center',
        textAlignVertical:'center'
    },

    /**
     * Show pending orders page
     */
    orderContainer:{
        width: "100%",
        backgroundColor: "lightgrey",
        borderRadius:5,
        marginVertical : "2%",
    },
    orderNumberText : {
        paddingHorizontal : '5%',
        fontSize : 16,
        marginTop : '5%',
        fontWeight:"bold"
    },
    orderInfoText : {
        flex: 1,
        paddingHorizontal : '5%',
        fontSize : 16,
        marginTop : '2%',
        marginBottom: "5%"
    },
    requiredText: {
        color:'red',
        fontSize : 16,
    },

    /**
     * Active listing page
     */
    itemContainer:{
        width: "100%",
        height: width/4,
        backgroundColor: "lightgrey",
        borderRadius:5,
        marginVertical : "2%",
    },
    itemCoverView:{
        width: width/4,
    },
    itemCover:{
        width: width/4,
        height: width/4,
        borderTopLeftRadius: 5,
        borderBottomLeftRadius: 5,
        position:'absolute',
        left:0,
        top: 0,
        bottom:0
    },
    itemTitleView:{
        flexDirection:"column",
        width: "60%",
        marginVertical : '5%',
        marginHorizontal: "3%",
    },
    itemTitle : {
        fontSize : 16,
        marginBottom: "2%",
        fontWeight:"bold",
    },
    itemPrice:{
        fontSize : 16,
        marginTop: "2%",
    },

    /**
     * Manual input popup
     */
    manualBackground:{
      width:width,
      height:height
    },
    manualPopup: {
        width: "100%",
        height: "40%",
        borderTopLeftRadius:10,
        borderTopRightRadius:10,
        position:"absolute",
        bottom:"10%",
        backgroundColor:'rgba(255,255,255,0.8)',
    },
    manualCloseButton:{
        position:"absolute",
        width:"5%",
        top:"5%",
        right:"5%",
    },
    manualPopupTitle: {
        marginTop:"10%",
        marginLeft:"10%",
        fontSize: 20,
        color: "black",
        fontWeight: "bold",
    },
    manualISBNInput : {
        width : '80%',
        borderColor: 'grey',
        paddingHorizontal : '5%',
        borderWidth: 1,
        fontSize : 18,
        marginVertical : '2%',
        marginLeft:"10%",
        padding : '2%',
    },
    searchButton : {
        width: "50%",
        marginVertical : '4%',
        marginLeft:"25%",
        padding : '3%',
        color: 'white',
        backgroundColor: colors.loginButton,
        alignItems : 'center'
    },

    //checkout popup
    checkoutPopup: {
        width: "100%",
        height: "35%",
        borderTopLeftRadius:10,
        borderTopRightRadius:10,
        position:"absolute",
        bottom:0,
        // shadowOffset:{width:10, height:10},
        // shadowColor:'lightgrey',
        backgroundColor:'rgba(255,255,255, 1)',
    },
    itemInfo:{
        flexDirection: "row",
        marginHorizontal: "5%",
        backgroundColor:"lightgrey",
        height: width/4,
        borderRadius: 10,
    },
    buttonView:{
        flexDirection: "row",
        marginHorizontal: "5%",
        justifyContent:"space-around",
    },
    removeButton : {
        width: "45%",
        marginVertical : '4%',
        marginHorizontal:"2%",
        paddingVertical : '3%',
        color: 'grey',
        fontSize:30,
        backgroundColor: colors.loginButton,
        alignItems : 'center'
    },
    modalView:{
        backgroundColor:"#000000aa",
        flex: 1,
        alignItems:"center",
        justifyContent:"center"
    },
    noIsbnPopup: {
        width: "90%",
        height: "30%",
        borderRadius:10,
        justifyContent:"center",
        backgroundColor:'rgba(255,255,255, 1)',
    },

    //orderItemDetails
    scrollContainer : {
        flexDirection: 'column',
        paddingHorizontal:"5%",
        width:"100%",
        height:"80%",
    },

    //warning popup
    warningText:{
        fontSize:16,
        color:"red",
        // marginBottom:"2%",
    },

    //orderItemDetails
    summaryContainer: {
        width: "60%",
        marginBottom:"3%",
        position:"relative",
        left: "40%",
    },

    summaryText: {
        textAlign: "right",
        marginVertical: "3%",
        fontSize: 18
    }

})
export default styles

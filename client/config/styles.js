import {StyleSheet} from "react-native";
import colors from "./colors";
const styles = StyleSheet.create({
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
        alignSelf : 'center'
    },
    textInput : {
        width : '100%',
        borderColor: 'black',
        paddingHorizontal : '10%',
        borderWidth: 1,
        fontSize : 16,
        marginVertical : '2%',
        padding : '2%'
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
    }
})
export default styles

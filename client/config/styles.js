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
    }
})
export default styles

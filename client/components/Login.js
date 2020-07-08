import React, { useState }  from 'react';
import { Text, View, Image, TextInput, TouchableOpacity} from 'react-native';
import { KeyboardAwareScrollView } from 'react-native-keyboard-aware-scroll-view'
import images from "../config/images";
import styles from "../config/styles";

export default function Login({navigation}){
    const [data, setData] = useState({
        email:'',
        password:'',
        emailError:false,
        loginError:false
    });

    const handleEmailChange = (val) => {
        setData({
            ...data,
            email: val,
            emailError: false,
            loginError:false
        })
    }
    const handlePasswordChange = (val) => {
        setData({
            ...data,
            password: val,
            loginError:false
        })
    }
    const validateEmail = () => {
        const re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
        if(!re.test(String(data.email).toLowerCase())){
            setData({
                ...data,
                emailError: true,
                loginError:false
            })
        }
    }
    const handleLogin = () => {
        if(data.email === 'adi@gmail.com' && data.password === '123'){
            navigation.navigate('rootNavigator')
        }else{
            setData({
                ...data,
                loginError: true
            })
        }
    }
    return(
        <KeyboardAwareScrollView>
            <Image  source={images.logo} style={styles.image}/>
            <View>
                <TextInput
                    placeholder='Username'
                    style={styles.textInput}
                    onChangeText={val => handleEmailChange(val)}
                    onBlur={() => validateEmail()}
                    keyboardType='email-address'
                    autoCorrect={false}
                    onSubmitEditing={()=>this.password.focus()}
                    blurOnSubmit={false}
                />
                {data.emailError?
                    <Text style={{color:'red'}}>Invalid email</Text>
                    : null
                }
                <TextInput
                    placeholder='Password'
                    style={styles.textInput}
                    onChangeText={val => handlePasswordChange(val)}
                    secureTextEntry={true}
                    ref={(input)=>this.password=input}
                    blurOnSubmit={false}
                />
                <TouchableOpacity activeOpacity={0.7} onPress={() => handleLogin()} title="Login" style={styles.loginButton}>
                    <Text style={styles.loginText}>LOGIN</Text>
                </TouchableOpacity>
                {data.loginError?
                    <Text style={{color:'red'}}>Invalid credentials</Text>
                    : null
                }
                <Text onPress={() => navigation.navigate('rootNavigator')} style={styles.resetAccountButton}>I don't have an account</Text>
            </View>
        </KeyboardAwareScrollView>
    )
}

import React, { useState }  from 'react';
import { Text, View, Image, TextInput, TouchableOpacity,Alert} from 'react-native';
import { KeyboardAwareScrollView } from 'react-native-keyboard-aware-scroll-view'
import images from "../config/images";
import styles from "../config/styles";

import api ,{setClientToken} from "../config/axios";

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
        if(data.email.length>0 && !re.test(String(data.email).toLowerCase())){
            setData({
                ...data,
                emailError: true,
                loginError:false
            })
        }
    }
    const handleLogin = () => {
        api.post('/login', {
            email: data.email,
            password: data.password
          })
          .then(function (response) {
              if (response.status === 200) {
                  setClientToken(response.data.token);
                  navigation.navigate('RootNavigator')
              } else {
                  setData({
                      ...data,
                      loginError: true
                  })
              }
          })
          .catch(function (error) {
            console.log(error.message);
            Alert.alert("Unable to connect to server. Please try later...")
          })

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
                    blurOnSubmit={false}
                />
                <TouchableOpacity activeOpacity={0.7} onPress={() => handleLogin()} title="Login" style={styles.loginButton}>
                    <Text style={styles.loginText}>LOGIN</Text>
                </TouchableOpacity>
                {data.loginError?
                    <Text style={{color:'red'}}>Invalid credentials</Text>
                    : null
                }
                <Text onPress={() =>
                    Alert.alert("Please contact your manager to create an account for you.")
                } style={styles.resetAccountButton}>I don't have an account</Text>
            </View>
        </KeyboardAwareScrollView>
    )
}

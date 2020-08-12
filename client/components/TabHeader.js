import React from 'react';
import { View } from 'react-native';
import SearchHeader from 'react-native-search-header';
import {Header, Left, Right, Icon} from "native-base";
import {
    Menu,
    MenuOptions,
    MenuOption,
    MenuTrigger,
} from 'react-native-popup-menu';
export default function TabHeader({navigation}){

    const searchHeaderRef = React.useRef(null);
    return(
        <View>
            <Header style={{backgroundColor:'white'}}>
                <Left>
                    <Icon onPress={() => navigation.toggleDrawer()} name='menu' style={{marginHorizontal:'5%'}}/>
                </Left>
                <Right>
                    <Icon onPress={() => searchHeaderRef.current.show()} name='search' style={{marginHorizontal:'8%'}}/>
                    {/* LISTING MENU COMMENTED FOR FUTURE USE*/}
                    {/*<Menu>*/}
                    {/*    <MenuTrigger>*/}
                    <Icon onPress={() => navigation.navigate('CameraTab', {mode: "add"})} name="add" style={{marginHorizontal:'8%'}}/>
                    {/*</MenuTrigger>*/}
                    {/*<MenuOptions optionsContainerStyle={styles.contextMenuContainer}>*/}
                    {/*    <MenuOption onSelect={() => this.props.navigation.navigate('CameraTab')}>*/}
                    {/*<TouchableOpacity*/}
                    {/*    style={{*/}
                    {/*        flex:1,*/}
                    {/*        justifyContent:'center',*/}
                    {/*        backgroundColor:'grey',*/}
                    {/*        alignItems:'center',*/}
                    {/*        padding:'5%'*/}
                    {/*    }}*/}
                    {/*    >*/}

                    {/*<Text style={styles.contextMenuText}>List a book</Text>*/}
                    {/*</TouchableOpacity>*/}
                    {/*</MenuOption>*/}
                    {/*<MenuOption>*/}
                    {/*    <Text style={styles.contextMenuText}>List clothing</Text>*/}
                    {/*<TouchableOpacity*/}
                    {/*    style={{*/}
                    {/*        flex:1,*/}
                    {/*        justifyContent:'center',*/}
                    {/*        backgroundColor:'grey',*/}
                    {/*        alignItems:'center',*/}
                    {/*        padding:'5%'*/}
                    {/*    }}>*/}
                    {/*    <Text style={{ fontSize: 24, color: 'white'}}>List clothing</Text>*/}
                    {/*</TouchableOpacity>*/}
                    {/*        </MenuOption>*/}
                    {/*    </MenuOptions>*/}
                    {/*</Menu>*/}
                </Right>
            </Header>
            <SearchHeader
                ref = { searchHeaderRef }
                placeholder = 'Enter ISBN or title...'
                placeholderColor = 'gray'
                pinnedSuggestions = {[]}
                // onClear = {() => {
                //     console.log(`Clearing input!`);
                // }}
                enableSuggestion={true}
                onGetAutocompletions = {async (text) => {
                    if (text) {
                        const response = await fetch(`http://suggestqueries.google.com/complete/search?client=chrome&q=${text}`, {
                            method: `get`
                        });
                        const data = await response.json();
                        return data[1];
                    } else {
                        return [];
                    }
                }}
                onHide={() => {
                    searchHeaderRef.current.clear()
                    navigation.navigate("Dashboard",{
                        screen:'Pending Orders',
                        refresh: true
                    })
                }}
                onSearch={(obj) => {
                    // update the active listing
                    navigation.navigate("Active Listing",{search:obj.nativeEvent.text})
                }}
            />
        </View>
    )
}

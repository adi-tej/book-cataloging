import React,{Component} from 'react';
import { NavigationActions, StackActions } from 'react-navigation';

import { Text, View} from 'react-native';
export default function Logout({navigation}) {
    return(
        <View>
            <Text>This is logout</Text>
        </View>
    )
}
// export default class Logout extends Component {
//     constructor(props) {
//         super(props);
//     }
//
//     componentWillMount() {
//         const resetAction = NavigationActions.reset({
//             index: 0,
//             key: null,
//             actions: [NavigationActions.navigate({ routeName: 'Landing' })]
//         })
//         this.props.navigation.dispatch(resetAction);
//     }
//     // render() {
//     //     return this.props.navigation.navigate('Landing');
//     // }
// }
// export default function Logout(navigation){
//     // const actionToDispatch = NavigationActions.reset({
//     //     index: 0,
//     //     key: null,
//     //     actions: [NavigationActions.navigate({ routeName: 'Landing' })]
//     // })
//     navigation.navigate('Landing');
// }

import React, {Component} from 'react';
import api from "../config/axios";
export default class Logout extends Component {

    componentDidMount(){
        api.post('logout')
            .then( res =>{
                if(res.status === 200){
                    this.props.navigation.navigate('Landing')
                }else{
                    console.log('Logout Failed')
                    alert('Logout Failed')
                }
            })
    }

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

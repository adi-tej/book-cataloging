import React, {Component} from 'react';
import {
    ScrollView,
    RefreshControl,
} from "react-native";
import styles from "../config/styles";
import ShowActiveListing from "./ShowActiveListing";
import api from "../config/axios";

export default class ActiveListing extends Component {
    constructor(props) {
        super(props);
        this.state = {infoArray:[],
            refreshing: false,
        }
    }

    getAllItems = () =>{
        api.get(`/book`)
            .then(res => {
                if(res.status === 200) {
                    this.setState({ infoArray: res.data.books});
                }else{
                    alert('Failed to get books')
                    console.warn('failed to get books')
                }
            }).catch((error)=>{
            console.warn(error.message);
        });
    }

    componentDidMount() {
        this.getAllItems()
    }

    componentWillReceiveProps(nextProps) {
        // Header search handling
        if (nextProps.route.params.search != null) {
            api.get(`/book`, {
                params: {
                    search: nextProps.route.params.search
                }
            })
                .then(res => {
                    if (res.status === 200) {
                        this.setState({infoArray: res.data.books});
                    } else {
                        alert('Failed to search')
                        console.warn('failed to search')
                    }
                }).catch((error) => {
                    console.warn(error.message);
            });
        }
        if (nextProps.route.params.refresh) {
            this.getAllItems()
        }

    }

    refreshNewItems = () => {
        this.setState({refreshing: true})
        setTimeout(
            () => {
                this.getAllItems()
                this.setState({refreshing: false})
            }
            , 1000)
    }

    render() {
        return (
            <ScrollView
                style={styles.container}
                refreshControl={
                    <RefreshControl refreshing={this.state.refreshing}
                                    onRefresh={this.refreshNewItems.bind(this)}
                    />
                }
            >
                {
                    this.state.infoArray.map((info, index)=>{
                        return(
                            <ShowActiveListing
                                key={info.id}
                                book={info}
                                navigation={this.props.navigation}
                            />
                        )
                    })
                }
            </ScrollView>
        );
    }
}

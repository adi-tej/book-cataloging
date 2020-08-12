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
        this.updateid = "";
        this.updateBookCover = "";
        this.updateTitle = "";
        this.updateAuthor = "";
        this.updateGenre = "";
        this.updatePrice = 0;
        //TODO: All details of the book
        this.state = {infoArray:[
                // {id: 1, cover: "https://picsum.photos/id/237/200/300", title:"Shanghai Girls is a 2009 novel by Lisa See. " +
                //         "It centers on the complex relationship between two sisters", author:"Tom", genre:"Novel", price: 10},
                // {id: 2, cover: "https://picsum.photos/seed/picsum/200/300", title:"Shanghai: This is a beautiful city,Cool",
                //  author:"Tom", genre:"Novel", price: 100},
                // {id: 3, cover: "https://picsum.photos/200/300?grayscale", title:"Shanghai", author:"Tom",
                //     genre:"Novel", price: 1.2},
                // {id: 4, cover: "https://picsum.photos/200/300/?blur", title:"Flower", author:"Tom",
                //     genre:"Science", price: 10.23},
                // {id: 5, cover: "https://picsum.photos/id/870/200/300?grayscale&blur=2", title:"Light tower",
                //     author:"Tom", genre:"Non-fiction", price: 10.456},
            ],
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
    //TODO: API call to get data before rendering
    componentDidMount() {
        // setClientToken("eyJhbGciOiJIUzUxMiJ9.eyJ1c2VyX2lkIjoxLCJ1c2VyX2VtYWlsIjoiYWRtaW5AY2lyY2V4LmNvbSIsInVzZXJfbmFtZSI6IkFkbWluIiwiZ2VuZXJhdGVfdGltZSI6MTU5Njk4OTY2MS4wMDA2MDR9.edaZGWGNYW7-POkcI0YpI6CHEXux9xj-7Y9g_lCS2B_sneUOtMLEz9d7UKMyH7ufwERjG76BqIrodOZtDf7afw")
        this.getAllItems()
    }
    //TODO: API call to Update state from search
    componentWillReceiveProps(nextProps) {
        //keyword from search
        //console.warn(this.props.route.params)
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

    //This function is to add a new order
    // addNewListingItem = () => {
    //     const copyInfoArray = Object.assign([], this.state.infoArray);
    //     copyInfoArray.push({
    //         id: this.updateid,
    //         cover: this.updateBookCover,
    //         title: this.updateTitle,
    //         author: this.updateAuthor,
    //         genre: this.updateGenre,
    //         price: this.updatePrice
    //     })
    //     this.setState({
    //         infoArray: copyInfoArray
    //     })
    // }

    refreshNewItems = () => {
        this.setState({refreshing: true})
        setTimeout(
            () => {
                this.getAllItems()
                this.setState({refreshing: false})
            }
            , 1000)
    }

    //TODO: set all fields to prop
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

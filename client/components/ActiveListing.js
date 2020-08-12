import React, {Component} from 'react';
import {ScrollView} from "react-native";
import styles from "../config/styles";
import ShowActiveListing from "./ShowActiveListing";
import api,{setClientToken} from "../config/axios";

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
                {id: 1, cover: "https://picsum.photos/id/237/200/300", title:"Shanghai Girls is a 2009 novel by Lisa See. " +
                        "It centers on the complex relationship between two sisters", author:"Tom", genre:"Novel", price: 10},
                {id: 2, cover: "https://picsum.photos/seed/picsum/200/300", title:"Shanghai: This is a beautiful city,Cool",
                 author:"Tom", genre:"Novel", price: 100},
                {id: 3, cover: "https://picsum.photos/200/300?grayscale", title:"Shanghai", author:"Tom",
                    genre:"Novel", price: 1.2},
                {id: 4, cover: "https://picsum.photos/200/300/?blur", title:"Flower", author:"Tom",
                    genre:"Science", price: 10.23},
                {id: 5, cover: "https://picsum.photos/id/870/200/300?grayscale&blur=2", title:"Light tower",
                    author:"Tom", genre:"Non-fiction", price: 10.456},
            ]}
    }

    //TODO: API call to get data before rendering
    componentDidMount() {
        // setClientToken("eyJhbGciOiJIUzUxMiJ9.eyJ1c2VyX2lkIjoxLCJ1c2VyX2VtYWlsIjoiYWRtaW5AY2lyY2V4LmNvbSIsInVzZXJfbmFtZSI6IkFkbWluIiwiZ2VuZXJhdGVfdGltZSI6MTU5Njk4OTY2MS4wMDA2MDR9.edaZGWGNYW7-POkcI0YpI6CHEXux9xj-7Y9g_lCS2B_sneUOtMLEz9d7UKMyH7ufwERjG76BqIrodOZtDf7afw")
        api.get(`/book`)
            .then(res => {
                if(res.status === 200) {
                    // console.warn(res)
                    // const books = res.data.books
                    // books.forEach( book => {
                    //     book.isbn = book.ISBN_10 ? book.ISBN_10 : book.ISBN_13
                    // })
                    this.setState({ infoArray: res.data.books});
                }else{
                    console.warn('error')
                }
            }).catch((error)=>{
                console.warn(error.message);
        });

    }
    //TODO: API call to Update state from search
    componentDidUpdate(prevProps, prevState, snapshot) {
        //keyword from search
        //console.warn(this.props.route.params)
        if(this.props.route && this.props.route.params) {
            if (this.props.route.params.search) {
                api.get(`/book`, {
                    params: {
                        search: this.props.route.params.data
                    }
                })
                    .then(res => {
                        if (res.status === 200) {
                            // console.warn(res)
                            // const books = res.data.books
                            // books.forEach(book => {
                            //     book.isbn = book.ISBN_10 ? book.ISBN_10 : book.ISBN_13
                            // })
                            this.setState({infoArray: res.data.books});
                        } else {
                            console.warn('error')
                        }
                    }).catch((error) => {
                        console.warn(error.message);
                });
            }
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
    //TODO: set all fields to prop
    render() {

        //console.warn(this.props.route.params)
        //this.props.navigation.routes.params.update();
        return (
            <ScrollView style={styles.container}>
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

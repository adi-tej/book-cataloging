import React, {Component} from 'react';
import {ScrollView} from "react-native";
import styles from "../config/styles";
import ShowActiveListing from "./ShowActiveListing";

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
                {id: 1, bookCover: "https://picsum.photos/id/237/200/300", title:"Shanghai Girls is a 2009 novel by Lisa See. " +
                        "It centers on the complex relationship between two sisters", author:"Tom", genre:"Novel", price: 10},
                {id: 2, bookCover: "https://picsum.photos/seed/picsum/200/300", title:"Shanghai: This is a beautiful city,Cool",
                 author:"Tom", genre:"Novel", price: 100},
                {id: 3, bookCover: "https://picsum.photos/200/300?grayscale", title:"Shanghai", author:"Tom",
                    genre:"Novel", price: 1.2},
                {id: 4, bookCover: "https://picsum.photos/200/300/?blur", title:"Flower", author:"Tom",
                    genre:"Science", price: 10.23},
                {id: 5, bookCover: "https://picsum.photos/id/870/200/300?grayscale&blur=2", title:"Light tower",
                    author:"Tom", genre:"Non-fiction", price: 10.456},
            ]}
    }

    //TODO: API call to get data before rendering
    componentDidMount() {
        // axios.get(`http://localhost/books`)
        //     .then(res => {
        //         const data = res.data;
        //         this.setState({ infoArray: data.infoArray });
        //     })
    }
    //This function is to add a new order
    addNewListingItem = () => {
        const copyInfoArray = Object.assign([], this.state.infoArray);
        copyInfoArray.push({
            id: this.updateid,
            bookCover: this.updateBookCover,
            title: this.updateTitle,
            author: this.updateAuthor,
            genre: this.updateGenre,
            price: this.updatePrice
        })
        this.setState({
            infoArray: copyInfoArray
        })
    }
    //TODO: set all fields to prop
    render() {
        return (
            <ScrollView style={styles.container}>
                {
                    this.state.infoArray.map((info, index)=>{
                        return(
                            <ShowActiveListing
                                key={info.id}
                                bookCover={info.bookCover}
                                title={info.title}
                                author={info.author}
                                genre={info.genre}
                                price={info.price}
                                navigation={this.props.navigation}
                            />
                        )
                    })
                }
            </ScrollView>
        );
    }
}

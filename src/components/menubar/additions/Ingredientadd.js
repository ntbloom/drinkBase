// Ingredientadd
// adds ingredient search bar to "add a drink" component

import React, { Component } from "react";

class Ingredientadd extends Component {
  constructor(props) {
    super(props)
    this.state = {
      Ingredient: '',
      Amount: '',
      Unit: '',
    }
    this.handleChange = this.handleChange.bind(this);
  }
  handleChange(event) {
    this.setState({[event.target.name]: event.target.value});
    console.log("state: ", this.state);
  }
  render() {
    return (
        <div>
        <input
          type="text"
          placeholder=" ingredient name"
          name="Ingredient"
          onChange={this.handleChange}
        >
        </input>
        <input
          type="text"
          placeholder=" amount (decimals only)"
          name="Amount"
          onChange={this.handleChange}
        >
        </input>
        <select
          name="Unit"
          onChange={this.handleChange}
        >
          <option value="oz">oz</option>
          <option value="dashes">dashes</option>
          <option value="each">each</option>
          <option value="garnish">garnish</option>
        </select>
      </div>
    );
  }
};

export default Ingredientadd;
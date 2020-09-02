import React, { Component } from 'react'

class Search extends Component {
  state = {
    query: '',
  }

  getInfo = (event) => {
    event.preventDefault();
    this.props.submitSearch(this.state.query)
  }

  handleInputChange = () => {
    this.setState({
      query: this.search.value
    })
  }

  render() {
    return (
      <form onSubmit={this.getInfo}>
        <div className="field">
          <input
            className="input"
            type="text"
            placeholder="Search questions..."
            ref={input => this.search = input}
            onChange={this.handleInputChange}
          />
        </div>        
        <a className="button is-info">Search</a>
      </form>
    )
  }
}

export default Search

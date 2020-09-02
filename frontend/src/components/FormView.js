import React, { Component } from 'react';
import $ from 'jquery';

import '../stylesheets/FormView.css';

class FormView extends Component {
  constructor(props){
    super();
    this.state = {
      question: "",
      answer: "",
      difficulty: 1,
      category: 1,
      categories: {}
    }
  }

  componentDidMount(){
    $.ajax({
      url: `/categories`, 
      type: "GET",
      success: (result) => {
        this.setState({ categories: result.categories })
        return;
      },
      error: (error) => {
        alert('Unable to load categories. Please try your request again')
        return;
      }
    })
  }


  submitQuestion = (event) => {
    event.preventDefault();
    $.ajax({
      url: '/questions',
      type: "POST",
      dataType: 'json',
      contentType: 'application/json',
      data: JSON.stringify({
        question: this.state.question,
        answer: this.state.answer,
        difficulty: this.state.difficulty,
        category: this.state.category
      }),
      xhrFields: {
        withCredentials: true
      },
      crossDomain: true,
      success: (result) => {
        document.getElementById("add-question-form").reset();
        return;
      },
      error: (error) => {
        alert('Unable to add question. Please try your request again')
        return;
      }
    })
  }

  handleChange = (event) => {
    this.setState({[event.target.name]: event.target.value})
  }

  render() {
    return (
      <div id="add-form" className="mt-4">
        <h2 className="title">Add a New Trivia Question</h2>
        <form className="form-view" id="add-question-form" onSubmit={this.submitQuestion}>
          <div className="field">
            <label>Question</label>
            <div className="control">
              <input className="input" type="text" name="question" onChange={this.handleChange}/>
            </div>
          </div>
          <div className="field">
            <label>Answer</label>
            <div className="control">
              <input className="input" type="text" name="answer" onChange={this.handleChange}/>
            </div>
          </div>
          <div className="field">
            <label>Difficulty </label>
            <div className="select">
              <select name="difficulty" onChange={this.handleChange}>
                <option value="1">1</option>
                <option value="2">2</option>
                <option value="3">3</option>
                <option value="4">4</option>
                <option value="5">5</option>
              </select>
            </div>

            <label>Category</label>
            <div className="select">
              <select name="category" onChange={this.handleChange}>
                {Object.keys(this.state.categories).map(id => {
                    return (
                      <option key={id} value={id}>{this.state.categories[id]}</option>
                    )
                  })}
              </select>
            </div>
          </div>
          <input type="submit" className="button" value="Submit" />
        </form>
      </div>
    );
  }
}

export default FormView;

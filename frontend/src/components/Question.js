import React, { Component } from 'react';
import '../stylesheets/Question.css';

class Question extends Component {
  constructor(){
    super();
    this.state = {
      visibleAnswer: false
    }
  }

  flipVisibility() {
    this.setState({visibleAnswer: !this.state.visibleAnswer});
  }

  render() {
    const { question, answer, category, difficulty } = this.props;
    return (
      <div className="columns">
        <div className="column">
          <div className="card">
            <div className="card-content">
              <p className="title">
                {question}
              </p>
              <p className="subtitle">
                <img className="category" src={`${category}.svg`}/>
                <div className="difficulty">Difficulty: {difficulty}</div>
                <span style={{"visibility": this.state.visibleAnswer ? 'visible' : 'hidden'}}>Answer: {answer}</span>
              </p>
            </div>
            <footer className="card-footer">
              <p className="card-footer-item">
                <a onClick={() => this.flipVisibility()}>{this.state.visibleAnswer ? 'Hide' : 'Show'} Answer</a>
              </p>
              <p className="card-footer-item">
                <img src="delete.png" className="delete" onClick={() => this.props.questionAction('DELETE')}/>
              </p>
            </footer>
          </div>
        </div>
      </div>
    );
  }
}

export default Question;

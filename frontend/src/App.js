import React, { Component } from 'react';
import {
  BrowserRouter as Router,
  Route,
  Switch
} from 'react-router-dom'

import './stylesheets/App.css';
import FormView from './components/FormView';
import QuestionView from './components/QuestionView';
import Header from './components/Header';
import QuizView from './components/QuizView';


class App extends Component {
  render() {
    return (
      <div>
        <Header path />
        <div className="container">
          <Router>
            <Switch>
              <Route path="/" exact component={QuestionView} />
              <Route path="/add" component={FormView} />
              <Route path="/play" component={QuizView} />
              <Route component={QuestionView} />
            </Switch>
          </Router>
        </div>
      </div>
    );
  }
}

export default App;

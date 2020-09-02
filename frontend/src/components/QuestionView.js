import React, { Component } from 'react';

import '../stylesheets/App.css';
import Question from './Question';
import Search from './Search';
import $ from 'jquery';

class QuestionView extends Component {
  constructor(){
    super();
    this.state = {
      questions: [],
      page: 1,
      totalQuestions: 0,
      categories: {},
      currentCategory: null,
    }
  }

  componentDidMount() {
    this.getQuestions();
  }

  getQuestions = () => {
    $.ajax({
      url: `/questions?page=${this.state.page}`,
      type: "GET",
      success: (result) => {
        this.setState({
          questions: result.questions,
          totalQuestions: result.total_questions,
          categories: result.categories,
          currentCategory: result.current_category })
        return;
      },
      error: (error) => {
        alert('Unable to load questions. Please try your request again')
        return;
      }
    })
  }

  selectPage(num) {
    this.setState({page: num}, () => this.getQuestions());
  }

  createPagination(){
    let pageNumbers = [];
    let maxPage = Math.ceil(this.state.totalQuestions / 10)
    for (let i = 1; i <= maxPage; i++) {
      pageNumbers.push(
        <a
          key={i}
          className={`page-num ${i === this.state.page ? 'active' : ''} pagination-link`}
          onClick={() => {this.selectPage(i)}}>{i}
        </a>)
    }
    return pageNumbers;
  }

  getByCategory= (id) => {
    $.ajax({
      url: `/categories/${id}/questions`,
      type: "GET",
      success: (result) => {
        this.setState({
          questions: result.questions,
          totalQuestions: result.total_questions,
          currentCategory: result.current_category })
        return;
      },
      error: (error) => {
        alert('Unable to load questions. Please try your request again')
        return;
      }
    })
  }

  submitSearch = (searchTerm) => {
    $.ajax({
      url: `/questions/search`, 
      type: "POST",
      dataType: 'json',
      contentType: 'application/json',
      data: JSON.stringify({searchTerm: searchTerm}),
      xhrFields: {
        withCredentials: true
      },
      crossDomain: true,
      success: (result) => {
        this.setState({
          questions: result.questions,
          totalQuestions: result.total_questions,
          currentCategory: result.current_category })
        return;
      },
      error: (error) => {
        alert('Unable to load questions. Please try your request again')
        return;
      }
    })
  }

  questionAction = (id) => (action) => {
    if(action === 'DELETE') {
      if(window.confirm('are you sure you want to delete the question?')) {
        $.ajax({
          url: `/questions/${id}`,
          type: "DELETE",
          success: (result) => {
            this.getQuestions();
          },
          error: (error) => {
            alert('Unable to load questions. Please try your request again')
            return;
          }
        })
      }
    }
  }

  render() {
    return (
      <section className="mt-5">
        <div className="tile is-ancestor">
          <div className="tile is-4">
            <aside className="menu">
              <p className="menu-label" onClick={() => {this.getQuestions()}}>Categories</p>
              <ul className="menu-list mb-5">
                {Object.keys(this.state.categories).map((id, ) => (
                  <li key={id} onClick={() => {this.getByCategory(id)}}>
                    {/* <figure className="image is-24x24">
                      <img src={`${this.state.categories[id]}.svg`}/>
                    </figure> */}
                    <a>{this.state.categories[id]}</a>
                  </li>
                ))}
              </ul>
              <Search submitSearch={this.submitSearch}/>
            </aside>
          </div>
          <div className="tile">
            <div className="questions-list">
              <h1 className="subtitle is-1">Questions</h1>
              {this.state.questions.map((q, ind) => (
                <Question
                  key={q.id}
                  question={q.question}
                  answer={q.answer}
                  category={this.state.categories[q.category]} 
                  difficulty={q.difficulty}
                  questionAction={this.questionAction(q.id)}
                />
              ))}
              <nav className="pagination is-centered" role="navigation" aria-label="pagination">
                <ul className="pagination-list">
                  <li>
                    {this.createPagination()}
                  </li>
                </ul>
              </nav>
            </div>
          </div>
        </div>
      </section>
    );
  }
}

export default QuestionView;

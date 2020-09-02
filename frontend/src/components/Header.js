import React, { Component } from 'react';
import '../stylesheets/Header.css';

class Header extends Component {

  navTo(uri){
    window.location.href = window.location.origin + uri;
  }

  render() {
    return (
      <section>
        <nav className="navbar is-dark" role="navigation" aria-label="main navigation">
          <div className="container">
            <div className="navbar-brand">
              <a className="navbar-item" onClick={() => {this.navTo('')}}>Udacitrivia</a>
            </div>
            <div className="navbar-menu">
              <div className="navbar-end">
                <div className="navbar-item">
                  <div className="field is-grouped">
                    <p className="control">
                      <a className="button is-success" onClick={() => {this.navTo('')}}>
                        <span>List</span>
                      </a>
                    </p>
                    <p className="control">
                      <a className="button is-info" onClick={() => {this.navTo('/add')}}>
                        <span>Add</span>
                      </a>
                    </p>
                    <p className="control">
                      <a className="button is-primary" onClick={() => {this.navTo('/play')}}>
                        <span>Play</span>
                      </a>
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </nav>
      </section>
    );
  }
}

export default Header;

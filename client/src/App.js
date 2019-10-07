import React from 'react';
import { BrowserRouter as Router, Switch, Route } from 'react-router-dom';
import { Provider } from 'react-redux'
import store from './store'

import Header from './components/common/Header'
import Footer from './components/common/Footer'
import TravelForm from './components/Forms/TravelForm'
import CurrentLocation from './components/GoogleMap/CurrentLocation'
import SearchResult from './components/SearchResult';
import GetLocation from './components/GoogleMap/GetLocation';
import ShowResult from './components/Result/ShowResult';
import SuccessBooking from './components/Result/SuccessBooking';
function App() {
  return (
    <Provider store={store}>
      <Router>
        <div className="App">
          <Header />

          <Switch>
            <Route exact path="/" component={TravelForm} />
            <Route exact path="/location" component={GetLocation} />
            <Route exact path="/result" component={ShowResult} />
            <Route exact path="/map" component={CurrentLocation} />
            <Route exact path="/success" component={SuccessBooking} />
            {/* <Route exact path='/search' component={SearchResult} /> */}
          </Switch>

          {/* <Footer /> */}
        </div>
      </Router>
    </Provider>
  );
}

export default App;

import React from 'react';
import { BrowserRouter as Router, Route } from 'react-router-dom';
import { routes } from './components/common/routeConfig';

class App extends React.Component {
  render() {
    return (
      <div className='App'>
        <Router>
          {routes.map((route, index) => (
            <Route 
              key={index}
              path={route.path}
              exact={route.exact}
              component={route.component}
            />
          ))}
        </Router>
      </div>
    );
  }
}

export default App;

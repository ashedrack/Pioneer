import React from 'react';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import ResourceMetrics from './components/ResourceMetrics';
import LogViewer from './components/LogViewer';
import ProcessMonitor from './components/ProcessMonitor';

const App = () => {
    return (
        <Router>
            <Switch>
                <Route path="/metrics" component={ResourceMetrics} />
                <Route path="/logs" component={LogViewer} />
                <Route path="/processes" component={ProcessMonitor} />
                <Route path="/" exact component={Home} />
            </Switch>
        </Router>
    );
};

export default App;

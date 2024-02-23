import React from 'react';
import {Route, Routes} from 'react-router-dom';
import './App.css';
import AuthWrapper from "./components/Auth/AuthWrapper";
import Layout from "./components/Layout/Layout";

function App() {
    return (
        <Routes>
            {/*<Route path="/auth" element={<AuthWrapper/>}/>*/}
            <Route path="/*" element={<Layout/>}/>
            {/*<Route path="/preview" element={<Preview />}/>*/}
        </Routes>
    );
}

export default App;

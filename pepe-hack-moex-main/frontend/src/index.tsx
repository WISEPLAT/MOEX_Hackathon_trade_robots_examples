import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';
import {BrowserRouter} from "react-router-dom";
import {ConfigProvider} from 'antd';

const root = ReactDOM.createRoot(
    document.getElementById('root') as HTMLElement
);
root.render(
    <React.StrictMode>
        <BrowserRouter>
            <ConfigProvider
                theme={{
                    "token": {
                        "colorPrimary": "#e50d0d",
                        "colorInfo": "#000000",
                        "colorSuccess": "#06AB03",
                        "colorWarning": "#ffd176",
                        "colorError": "#ff0002",
                        "fontSize": 16,
                        "sizeStep": 4,
                        "sizeUnit": 4,
                        "borderRadius": 10,
                        // fontFamily: 'Gilroy',
                    }
                }}
            >
                <App/>
            </ConfigProvider>
        </BrowserRouter>
    </React.StrictMode>
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
// reportWebVitals();

import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import {createBrowserRouter, RouterProvider,} from "react-router-dom";
import {AlgoPage, ErrorPage, MainPage} from "./pages";
import {getAllDatasets, getAlgo} from "./api/api";
import {ApiProvider} from '@reduxjs/toolkit/dist/query/react'
import {apiSlice} from './chat/store/api';
import {Provider} from 'react-redux'
import {store} from './chat/store/store';


const router = createBrowserRouter([
    {
        path: "/",
        element: <MainPage/>,
        errorElement: <ErrorPage/>,
    },
    // {
    //     path: "/uploaded-data",
    //     element: <UploadedDataPage/>,
    //     errorElement: <ErrorPage/>
    // },
    {
        path: '/algos/:algoName',
        element: <AlgoPage/>,
        loader: async ({params}) => {
            if (!params.algoName) throw new Response("Not Found", {status: 404});
            return getAlgo(params.algoName)
        },
        errorElement: <ErrorPage/>
    },
]);

const root = ReactDOM.createRoot(
    document.getElementById('root') as HTMLElement
);
root.render(
    <React.StrictMode>
        <ApiProvider api={apiSlice}>
            <Provider store={store}>
                <RouterProvider router={router}/>
            </Provider>
        </ApiProvider>
    </React.StrictMode>
);


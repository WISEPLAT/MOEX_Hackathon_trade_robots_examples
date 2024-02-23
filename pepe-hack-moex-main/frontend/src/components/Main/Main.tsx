import React from "react";
import {Divider} from "antd";
import Stocks from "./Stocks/Stocks";
import Carousel from "./Carousel/Carousel";
import News from "./News/News";

interface MainPropsType {}

const Main: React.FC<MainPropsType> = () => {
    return (
        <>
            <Stocks/>
            <Divider/>
            <Carousel/>
            <div style={{paddingBottom: 18}}/>
            <News/>
        </>
    );
};

export default Main;

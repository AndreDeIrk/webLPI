import React from "react";
import MyPlot from "./elements/Plot";
import "./styles/global.scss";
import "./styles/header.scss";
import "./styles/elements/plot.scss";

const Home = (props) => {

    return (
        <MyPlot data={1}
                row={2}
                title={'Graph #1'}
                xTitle={'Title X'}
                yTitle={'Title Y'}
                xAutorange={true}
                yAutorange={true}
                options={2}/>
    );
}

export default Home;
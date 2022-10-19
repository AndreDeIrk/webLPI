import React, { useEffect, useState } from "react";
import "./styles/global.scss";

class Home extends React.Component {

    render() {
        return (
            <div className={"body text " + this.props.className}>
                <div className={"header-bar"}>
                    <h2>Home</h2>
                </div>
                <div style={{
                    height: '4000px',
                    background: "rgba(0, 0, 0, 0)",
                    margin: '50px',
                }}>
                    My Home page!
                </div>
            </div>
        );
    }
}

export default Home;
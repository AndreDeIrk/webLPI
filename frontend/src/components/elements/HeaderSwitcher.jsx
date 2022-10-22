import React, { useEffect, useRef, useState }  from 'react';
import '../styles/header.scss';
import { Link } from "react-router-dom";

const HeaderSwitcher = (props) => {
    return (
        <Link to={`/${props.to.toLowerCase()}`}
              onClick={() => {props.onClick(`/${props.to.toLowerCase()}`)}}>
            <button className={"header-btn" + (props.page === `/${props.to.toLowerCase()}` ? " active" : "")}>
                {props.to}
            </button>
        </Link>
    )
}

export default HeaderSwitcher;
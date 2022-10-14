import React from 'react';
import '../styles/elements/buttons.scss';
import login from '../../imgs/login.svg';

export function ButtonSubmit(props) {
    return (
        <button type="submit"
                className="btn-submit"
                style={{width: props.width, height: props.height}}>
            {/*<svg className="spinner btn-img" viewBox="0 0 50 50">*/}
            {/*    <circle className="path"*/}
            {/*            cx="25"*/}
            {/*            cy="25"*/}
            {/*            r="20"*/}
            {/*            fill="transparent">*/}
            {/*    </circle>*/}
            {/*</svg>*/}
            <img className='btn-img' src={login} />
        </button>
)}

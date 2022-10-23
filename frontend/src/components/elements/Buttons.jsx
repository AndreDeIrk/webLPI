import React from 'react';
import '../styles/elements/buttons.scss';
import LoginImg from '../../imgs/login.svg';
import WarningImg from '../../imgs/warning.svg'

const Button = (props) => {

    return (
        <div className={"btn-block " + props.className}
             style={{height: props.size}}>
            <button type="button"
                    style={{width: props.size, height: props.size}}
                    onClick={props.onClick}
                    disabled={props.state !== 'login'}>
                {props.type === 'submit' &&
                <>
                    {props.state === 'loading' &&
                    <div className={'btn-img'}>
                        <svg className="spinner" viewBox="0 0 50 50">
                            <circle className="path"
                                    cx="25"
                                    cy="25"
                                    r="20"
                                    fill="transparent">
                            </circle>
                        </svg>
                    </div>}
                    {props.state === 'login'  &&
                    <img className={'btn-img'}
                         src={LoginImg}
                         alt={LoginImg}/>}
                    {props.state === 'warning'  &&
                    <img className={'btn-img'}
                         src={WarningImg}
                         alt={WarningImg}/>}
                </>}
            </button>
        </div>
    )

}

export default Button;
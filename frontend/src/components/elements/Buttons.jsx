import React, { useState } from 'react';
import '../styles/elements/buttons.scss';
import LoginImg from '../../imgs/login.svg';

export class ButtonSubmit extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            state: "login"
        }
        this.switchLoading= this.switchLoading.bind(this);
    }

    switchLoading(state : string) {
        this.setState({state: state});
    }

    render() {
        return (
            <div className={this.props.className}
                 style={{
                     display: "flex",
                     justifyContent: "center",
                     height: this.props.size,
                 }}>
                <button type="button"
                        className={"btn-submit"}
                        style={{width: this.props.size, height: this.props.size}}
                        onClick={this.props.onclick}>
                    <div className={'btn-img' + (this.state.state !== 'loading' ? " hidden" : "")}>
                        <svg className="spinner" viewBox="0 0 50 50">
                            <circle className="path"
                                    cx="25"
                                    cy="25"
                                    r="20"
                                    fill="transparent">
                            </circle>
                        </svg>
                    </div>
                    <img className={'btn-img' + (this.state.state !== 'login' ? " hidden" : "")}
                         src={LoginImg} />
                </button>
            </div>
        )
    }
}

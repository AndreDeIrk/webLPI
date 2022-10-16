import React from 'react';
import '../styles/elements/buttons.scss';
import LoginImg from '../../imgs/login.svg';
import WarningImg from '../../imgs/warning.svg'

export class Button extends React.Component {
    // constructor(props) {
    //     super(props);
    //     this.state = {
    //         submitState: "login"
    //     }
    //     this.switchSubmit = this.switchSubmit.bind(this);
    // }

    render() {
        return (
            <div className={"btn-block " + this.props.className}
                 style={{height: this.props.size}}>
                <button type="button"
                        style={{width: this.props.size, height: this.props.size}}
                        onClick={this.props.onclick}
                        disabled={this.props.state !== 'login'}>
                    {this.props.type === 'submit' &&
                    <>
                        {this.props.state === 'loading' &&
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
                        {this.props.state === 'login'  &&
                        <img className={'btn-img'}
                             src={LoginImg}
                             alt={LoginImg}/>}
                        {this.props.state === 'warning'  &&
                        <img className={'btn-img'}
                             src={WarningImg}
                             alt={WarningImg}/>}
                    </>}
                </button>
            </div>
        )
    }
}

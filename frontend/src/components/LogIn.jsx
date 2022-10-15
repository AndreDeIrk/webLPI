import React from "react";
import './styles/global.scss';
import { ButtonSubmit } from "./elements/Buttons";
// import Gear from "../imgs/gear.svg"

class LogIn extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            isSignIn: true,
            isInputTg: true,
        }
        this.hideForm = this.hideForm.bind(this);
    }

    hideForm() {
        this.setState({isSignIn: !this.state.isSignIn});
    }

    render() {
        return (
            <div className={"body " + this.props.className}>
                <div className={"login-box"}>
                    <form className={"login-form" + (!this.state.isSignIn ? " hide-left" : "")} >
                        <div className="form-item">
                            <div className="form-title">Sign In</div>
                        </div>
                        <div className="form-item">
                            <div className={'input-gp'}>
                                {/*<label htmlFor="tg-input" className={"input-label"}>TG:</label>*/}
                                <input name="userTg"
                                       id="tg-input"
                                       type="text"
                                       className={"input"}
                                       placeholder={'Telegram'}/>
                            </div>
                        </div>
                        <div className="form-item">
                            <div className={'input-gp'}>
                                <input name="userPw"
                                       id="pw-input"
                                       type="password"
                                       className="input"
                                       placeholder={'Password'}/>
                            </div>
                        </div>
                        <div className="form-item__grid last">
                            <ButtonSubmit size={'47px'}
                                          className={'center-1'}/>
                            <button className={'btn-link right-3'}
                                    onClick={(e) => {
                                        e.preventDefault();
                                        this.setState({
                                            isSignIn: false
                                        });
                                    }}>
                                Sign Up
                            </button>
                        </div>
                    </form>

                    <form className={"login-form" + (this.state.isSignIn ? " hide-right" : "")} >
                        <div className="form-item">
                            <div className="form-title">Sign Up</div>
                        </div>
                        <div className="form-item">
                            <div className={'input-gp'}>
                                <input name="userTg-new"
                                       id="tg-input-new"
                                       type="text"
                                       className={"input" + (!this.state.isInputTg ? " hide-top" : "")}
                                       placeholder={'Telegram'}/>
                                <input id="code"
                                       type="text"
                                       value={'0 1 2 3'}
                                       className={"input" + (this.state.isInputTg ? " hide-bottom" : "")}
                                       disabled/>
                            </div>
                        </div>
                        <div className="form-item"
                             style={{
                                 marginBottom: "2em",
                             }}>
                            <button className={'btn-link right-3'}
                                    onClick={(e) => {
                                        e.preventDefault();
                                        this.setState({isInputTg: !this.state.isInputTg});
                                    }}>
                                Get code
                            </button>
                        </div>
                        <div className="form-item last">
                            <button className={'btn-link right-3'}
                                    onClick={(e) => {
                                        e.preventDefault();
                                        this.setState({
                                            isSignIn: true,
                                            isInputTg: true,
                                        });
                                    }}>
                                Sign In
                            </button>
                        </div>
                    </form>
                </div>

                {/*<img src={Gear}*/}
                {/*     style={{width: '25%'}}*/}
                {/*     className={'spinner-img'}/>*/}

            </div>
        );
    }
}

export default LogIn;
import React from "react";
import PropTypes from "prop-types";
import './styles/global.scss';
import { Button } from "./elements/Buttons";
// import Gear from "../imgs/gear.svg"

class Login extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            isSignIn: true,
            isInputTg: true,
            loginState: 'login',
            username: "-",
            password: "-",
        }
        this.switchForm = this.switchForm.bind(this);
        this.submitForm = this.submitForm.bind(this);
    }

    async switchForm(event) {
        event.preventDefault();
        this.setState({isSignIn: !this.state.isSignIn});
    }

    async loginUser(credentials) {
        return fetch('http://localhost:8000/auth', {
             method: 'POST',
             headers: {
                 'Content-Type': 'application/json',
             },
             body: JSON.stringify(credentials)
        })
        .then(data => data.json()).catch((error) => {
            return {status: false, detail: error}
        })
    }

    async submitForm(event) {
        event.preventDefault();

        if (this.state.username === "-" || this.state.password === "-") {
            this.setState({
                username: (this.state.username === "-" ? "" : this.state.username),
                password: (this.state.password === "-" ? "" : this.state.password)
            });
        }
        else {
            const token = await this.loginUser({
                telegram: this.state.username,
                password: this.state.password
            })
            this.props.setToken({token: (token.status ? token['access_token'] : "")});
            if (!token.status) {
                console.log(token.detail);
            }
        }
    }

    componentDidUpdate(prevProps, prevState, snapshot) {
        // console.log(this.state.username);
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
                            <div className={'input-gp' + (this.state.username === "" ? ' warning' : "")}>
                                {/*<label htmlFor="tg-input" className={"input-label"}>TG:</label>*/}
                                <input name="username"
                                       id="tg-input"
                                       type="text"
                                       className={"input"}
                                       placeholder={'Telegram'}
                                       onChange={event => this.setState({username: event.target.value})}/>
                            </div>
                        </div>
                        <div className="form-item">
                            <div className={'input-gp' + (this.state.password === "" ? ' warning' : "")}>
                                <input name="password"
                                       id="pw-input"
                                       type="password"
                                       className="input"
                                       placeholder={'Password'}
                                       onChange={event => this.setState({password: event.target.value})}/>
                            </div>
                        </div>
                        <div className="form-item__grid last">
                            <Button size={'47px'}
                                    type={'submit'}
                                    state={this.state.loginState}
                                    onClick={(e) => {
                                        this.submitForm(e);
                                    }}
                                    className={'center-1'}/>
                            <button className={'btn-link right-3'}
                                    onClick={(e) => {
                                        this.switchForm(e);
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
                                <input name="newUsername"
                                       id="tg-input-new"
                                       type="text"
                                       className={"input" + (!this.state.isInputTg ? " hide-top" : "")}
                                       placeholder={'Telegram'}/>
                                <input id="code"
                                       name="code"
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
                                        this.switchForm(e);
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

Login.propTypes = {
    setToken: PropTypes.func.isRequired
}

export default Login;
import React from "react";
import PropTypes from "prop-types";
import './styles/global.scss';
import Button from "./elements/Buttons";
import Request from "./Request";
// import Gear from "../imgs/gear.svg"

class Login extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            isSignIn: false,
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
        this.setState({isSignIn: !this.state.isSignIn, isInputTg: true});
    }

    async loginUser(credentials) {
        return await Request('/auth', JSON.stringify(credentials));
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
            this.props.setToken(token.status ? token : {
                token: ""
            });
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
            <div className={'body ' + this.props.className} data-center>
                <div className={"switch-container dark"}>
                    <form data-hide-left={!this.state.isSignIn}
                          style={{width: '300px'}}
                          data-align="center">
                        <h1>Sign In</h1>
                        <input name="username" type="text" placeholder={'Telegram'}
                               onChange={event => this.setState({username: event.target.value})}
                               data-large/>
                        <input name="password" type="password" placeholder={'Password'}
                               onChange={event => this.setState({password: event.target.value})}
                               data-large/>
                        <div className="row">
                            <div className="col-3"></div>
                            <Button size={'47px'} type={'submit'} state={this.state.loginState}
                                    className='col-6'
                                    onClick={(e) => {
                                        this.submitForm(e);
                                    }}/>
                            <button className={'btn-link col-3'}
                                    onClick={(e) => {
                                        this.switchForm(e);
                                    }}>Sign Up</button>
                        </div>
                    </form>

                    <form data-hide-right={this.state.isSignIn}
                          style={{width: '300px'}}
                          data-align="center">
                        <h1 className="form-title">Sign Up</h1>
                        <div className="input-group switch-container" style={{width: '100%'}}>
                            <input name="newUsername"
                                   id="tg-input-new"
                                   type="text"
                                   data-hide-top={!this.state.isInputTg}
                                   data-align='center'
                                   data-large
                                   placeholder={'Telegram'}
                                   data-last/>
                            <input id="code"
                                   name="code"
                                   type="text"
                                   value={'0 1 2 3'}
                                   data-hide-bottom={this.state.isInputTg}
                                   data-align='center'
                                   data-large
                                   data-last
                                   disabled/>
                        </div>
                        <button className={'btn-link'}
                                onClick={(e) => {
                                    e.preventDefault();
                                    this.setState({isInputTg: !this.state.isInputTg});
                                }}>Get code</button>
                        <button className={'btn-link mt-5'}
                                onClick={(e) => {
                                    this.switchForm(e);
                                }}>Sign In</button>
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
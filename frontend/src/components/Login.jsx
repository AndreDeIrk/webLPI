import React, { useState } from "react";
import PropTypes from "prop-types";
import './styles/global.scss';
// import Button from "./elements/Buttons";
import Request from "./Request";

import Form from 'react-bootstrap/Form';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';

const Login = (props) => {
    const [ SI, setSI ] = useState(true);
    const [ SUcode, setSUcode ] = useState(false);
    const [ username, setUsername ] = useState('');
    const [ password, setPassword ] = useState('');

    async function switchForm(event, state) {
        event.preventDefault();
        setSI(state);
        setSUcode(false);
    }

    async function loginUser(credentials) {
        return await Request('/auth', JSON.stringify(credentials));
    }

    async function submitForm(event) {
        event.preventDefault();

        const token = await loginUser({
            telegram: username,
            password: password
        })
        props.setToken(token.status ? token : {
            token: ""
        });
        if (!token.status) {
            console.log(token.detail);
        }
        
    }

    
    return (
        <div className={`body ${props.className}`} data-center>
            <div className={"switch-container dark"}>
                <Form data-hide-left={!SI}
                        className="p-3">
                    <h1>Sign In</h1>
                    <Form.Control name="username" type="text"
                                    className="mb-3 web-input" 
                                    placeholder={'Telegram'}
                                    onChange={event => setUsername(event.target.value)}/>
                    <Form.Control name="password" type="password" 
                                    className="mb-3 web-input" 
                                    placeholder={'Password'}
                                    onChange={event => setPassword(event.target.value)}/>
                    <Row>
                        <Col>
                            <button type="submit"
                                    className='web-btn'
                                    onClick={(e) => {
                                        submitForm(e);
                                    }}>
                                Submit
                            </button> 
                        </Col>
                        <Col>
                            <div style={{display: 'flex', flexDirection: 'row-reverse'}}>
                                <button type="link"
                                        className='web-btn'
                                        onClick={(e) => {
                                            switchForm(e, false);
                                        }}>
                                    Sign Up
                                </button> 
                            </div>
                        </Col>
                    </Row>
                </Form>

                <Form data-hide-right={SI}
                        className='p-3'>
                    <h1 className="form-title">Sign Up</h1>
                    <Form.Control name="newUsername"
                                    className="web-input mb-3"
                                    type="text"
                                    placeholder={'Telegram'}
                                    data-last/>
                    <Form.Control name="code"
                                    className="web-input mb-3"
                                    type="text"
                                    value={'0 1 2 3'}
                                    disabled hidden={!SUcode}/>
                    <Row>
                        <Col>
                            <button type='link'
                                    onClick={(e) => {
                                        e.preventDefault();
                                        setSUcode(!SUcode);
                                    }}
                                    className={'web-btn'}>Get code</button>
                        </Col>
                        <Col>
                            <div style={{display: 'flex', flexDirection: 'row-reverse'}}>
                                <button type='link'
                                        className='web-btn'
                                        onClick={(e) => {
                                            switchForm(e, true);
                                        }}>Sign In</button>
                            </div>
                        </Col>
                    </Row>
                </Form>
            </div>
        </div>
    );
}

Login.propTypes = {
    setToken: PropTypes.func.isRequired
}

export default Login;
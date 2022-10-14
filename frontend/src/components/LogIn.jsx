import React, { useEffect, useState } from "react";
import './styles/global.scss';
import { ButtonSubmit } from "./elements/Buttons";

// const {tg, setTG} = useState()
class LogIn extends React.Component {

    render() {
        return (
            <div className={"body"}>
                <form className="login-form" >
                    <div className="form-item">
                        <div className="form-title">Log In</div>
                    </div>
                    <div className="form-item">
                        <label htmlFor="tg-input" className="form-input-label">TG:</label>
                        <input name="userTg" id="tg-input" type="text" className="form-input" required/>
                    </div>
                    <div className="form-item">
                        <label htmlFor="pw-input" className="form-input-label">PW:</label>
                        <input name="userPw" id="pw-input" type="password" className="form-input" required/>
                    </div>
                    <div className="form-item last">
                        <ButtonSubmit width={'70px'} height={'70px'}/>
                    </div>
                </form>
            </div>
        );
    }
}

export default LogIn;
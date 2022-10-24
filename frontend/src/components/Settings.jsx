import React from "react";
import "./styles/global.scss";

const Settings = () => (
    <div>
        Settings...
        <div className={'switch-container dark'}>
            <form>
                <div className="row">
                    <div className={'input-group col-6 me-1'}>
                        <label htmlFor='i1'>HEYfjhdkjhgd</label>
                        <input id="i1" data-align="center"/>
                        {/* <label htmlFor='i2'>@</label> */}
                        <input id='i2' data-align="end" data-last/>
                    </div>                    
                    <input className="col-6 ms-1" data-align='center'/>
                </div>
                <input className="" data-align='center'/>
            </form>
        </div>
    </div>
);

export default Settings;
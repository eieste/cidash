import EventDashboard from "./components/EventDashboard";
import './App.css';
import React, { useState } from "react";
import {CredentialContext, defaultCredential} from "./context";
import Cookies from 'universal-cookie';
import Login from "./components/Login";
const cookies = new Cookies();

function App() {
    let initialCredential = defaultCredential;
    let credential_cookie = cookies.get("cidash_credential");
    if(credential_cookie){
        initialCredential = credential_cookie;
    }
    const [credential, setCredential] = useState(initialCredential);

    return (
        <CredentialContext.Provider value={{credential, setCredential}}>

            <div className="App">
                {
                    (
                        () => {
                            if(credential.username == "" || credential.password == "" || credential.username == false || credential.password == false) {
                                return <Login />
                            } else {
                                return <EventDashboard />
                            }
                        }
                    )()
                }

            </div>
        </CredentialContext.Provider>
      );
}

export default App;

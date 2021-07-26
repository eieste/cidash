import EventDashboard from "./components/EventDashboard";
import './App.css';
import React, { useState } from "react";
import {CredentialContext, defaultCredential} from "./context";
import Cookies from 'universal-cookie';

const cookies = new Cookies();

function App() {
    let initialCredential = defaultCredential;
    let credential_cookie = cookies.get("cidash_credential");
    if(credential_cookie){
        initialCredential = credential_cookie;
    }
    const [credential, setCredential] = useState(initialCredential);
    const [credentialInput, setCredentialInput] = useState({"username": "", "password": ""});

    function handleInput(name, event){
        credentialInput[name] = event.target.value;
        setCredentialInput(credentialInput);
    }

    function handleSaveCredential(){
        setCredential(credentialInput);
        cookies.set('cidash_credential', JSON.stringify(credentialInput), {path: '/'});
    }

    return (
        <CredentialContext.Provider value={{credential, setCredential}}>

            <div className="App">
                {
                    (
                        () => {
                            if(credential.username == "" || credential.password == "" || credential.username == false || credential.password == false) {
                                return <div>
                                    Username: <input type="text" onInput={ (evt) => handleInput("username", evt)} /><br/>
                                    Passwort: <input type="password" onInput={ (evt) => handleInput("password", evt)}/><br/>
                                    <input type="button" value={"Speichern"} onClick={ (evt) => handleSaveCredential(evt)} /> 
                                </div>
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

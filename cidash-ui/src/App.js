import EventDashboard from "./components/EventDashboard";
import './App.css';
import React, { useState } from "react";

const defaultCredential = {
    "username": "asdf",
    "password": "",
};

export const CredentialContext = React.createContext({ 
    "credential": defaultCredential,
    "setCredential": () => {}
});


function App() {
    const [credential, setCredential] = useState(defaultCredential);
    const [credentialInput, setCredentialInput] = useState({"username": "", "password": ""});

    function handleInput(name, event){
        credentialInput[name] = event.target.value;
        setCredentialInput(credentialInput);
    }

    function handleSaveCredential(){
        setCredential(credentialInput);
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
                            }
                        else{
                            return <EventDashboard />
                        }
                   })()
                }

            </div>
        </CredentialContext.Provider>
      );
}

export default App;

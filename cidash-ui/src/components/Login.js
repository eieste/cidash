import React, { useState, useContext } from "react";
import { CredentialContext } from "../context.js";
import styles from "./Login.module.css";
import Cookies from 'universal-cookie';
const cookies = new Cookies();

function Login(){
    const [credentialInput, setCredentialInput] = useState({"username": "", "password": ""});
    const { setCredential } = useContext(CredentialContext);

    function handleInput(name, event){
        credentialInput[name] = event.target.value;
        setCredentialInput(credentialInput);
    }


    function handleSaveCredential(){
        setCredential(credentialInput);
        cookies.set('cidash_credential', JSON.stringify(credentialInput), {path: '/'});
    }

    return (
        <div className={styles.login} >
            <div className={styles.heading}>
                <h2 className={styles.headingH2}>Login</h2>
                <form action="#">
                    <div className={styles["input-group"]}>
                        <input type="text" onInput={ (evt) => handleInput("username", evt)} className={styles["form-control"]} placeholder="Username or email" />
                    </div>

                    <div className={styles["input-group"]}>
                        <input type="password" onInput={ (evt) => handleInput("password", evt)} className={styles["form-control"]} placeholder="Password" />
                    </div>
                    <button type="submit" onClick={ (evt) => handleSaveCredential(evt)} className={styles.submitButton}>Login</button>
                </form>
            </div>
        </div>);
}



export default Login;

import React from "react";



const defaultCredential = {
    "username": "asdf",
    "password": "",
};

const CredentialContext = React.createContext({ 
    "credential": defaultCredential,
    "setCredential": () => {}
});

const defaultEventData = {
    "eventSource": [],
    "version":"",
    "eventResource": []
};

const EventContext = React.createContext({
		eventData: defaultEventData, 
		setEventData: () => {},
});


export {
    defaultCredential,
    CredentialContext,
    defaultEventData,
    EventContext,
}

import React from "react";
import _ from "lodash";

export function getData(path, options){
    const credential = _.get(options, "credential", {"username": "", "password":""});
    _.remove(options, "credential");
    _.set(options, ["headers", "Authorization"], "Basic "+btoa(credential.username+":"+credential.password));

    let config = false;
    if (process.env.NODE_ENV === "development") {
        config = require("./localconfig.json");
    }else{
        config = require("./config.json");
    }
        
    

    return fetch(config["api_endpoint_url"]+path, options)
        .then( response => response.json())
        .then( (jsonData) => {
            if( jsonData.version !== config.version  ){
                throw "Invalid Event Version";
            }
            return jsonData;
        })
}

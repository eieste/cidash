import React from "react";
import config from "./config.json";
import _ from "lodash";

export function getData(path, options){
    const credential = _.get(options, "credential", {"username": "", "password":""});
    _.remove(options, "credential");
    _.set(options, ["headers", "Authorization"], "Basic "+btoa(credential.username+":"+credential.password));

    return fetch(config["api_endpoint_url"]+path, options)
        .then( response => response.json())
        .then( (jsonData) => {
            if( jsonData.version !== config.version  ){
                throw "Invalid Event Version";
            }
            return jsonData;
        })
}

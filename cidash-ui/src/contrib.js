import config from "./config.json";

export function getData(path, options){
    return fetch(config["api_endpoint_url"]+path, options)
        .then( response => response.json())
        .then( (jsonData) => {
            if( jsonData.version !== config.version  ){
                throw "Invalid Event Version";
            }
            return jsonData;
        })
}

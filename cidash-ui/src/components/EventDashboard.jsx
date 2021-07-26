import React from "react";
import { useState, useEffect, useContext } from "react";
import Group from "./Group";
import config from "../config.json";
import {getData} from "../contrib.js";
import _ from "lodash";
import {defaultEventData, EventContext, CredentialContext} from "../context";

function EventDashboard(){
    const [eventData, setEventData] = useState(defaultEventData);
    const { credential } = useContext(CredentialContext);

    useEffect( () => {
        getData("/data", {credential}).then( (jsonData) => {
            setEventData(jsonData);
        });

        let i = 0;
        const interval = setInterval(function(){
            i++;
            let percent = i/config.refreshInterval*100;
            if(percent => 99){
                getData("/data", {credential}).then( (jsonData) => {
                    setEventData(jsonData);
                    i = 0;
                });
            }
        }, 100);
    }, []);

    return (
        <EventContext.Provider value={{eventData, setEventData}} >
            <div>
                {
                    (
                        () => {
                            let groupList = [];
                            _.forEach(eventData.eventSource, function(eventSource) {
                            console.log(eventSource);
                                let groupEvents = _.filter(eventData.eventResource, (item) => { return item.eventSource === eventSource["slug"] });
                                groupList.push( <Group displayName={eventSource.displayName} slug={eventSource.slug} events={groupEvents} /> );   
                            })
                            return groupList;
                        }

                    )()
                }


            </div>
        </EventContext.Provider>
  );
}

export default EventDashboard;

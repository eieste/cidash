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
    const [percent, setPercent] = useState(100);
    const [ timeInterval, setTimeInterval] = useState(0);

    useEffect( () => {
        let stepSize = 100;
        const interval = setInterval(() => {
            setTimeInterval(timeInterval => timeInterval + stepSize );
        }, stepSize);
        return () => clearInterval(interval);
    });

    useEffect(() => {
        let percent = ( timeInterval / config.refreshInterval ) * 100;
        console.log(percent);
        if(percent >= 99) {
            percent = 0
            getData("/data", {credential}).then( (jsonData) => {
                setEventData(jsonData);
            });
            setTimeInterval(0);
        }
        setPercent( percent );
    }, [timeInterval])

    return (
        <EventContext.Provider value={{eventData, setEventData}} >
            <div>
                {
                    (
                        () => {
                            let groupList = [];
                            _.forEach(eventData.eventSource, function(eventSource) {
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

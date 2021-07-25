import React from "react";
import { useState, useEffect } from "react";
import Group from "./Group";
import config from "../config.json";
import {getData} from "../contrib.js";
import _ from "lodash";


const defaultEventData = {
    "eventSource": [],
    "version":"",
    "eventResource": []
};

export const EventContext = React.createContext({
		eventData: defaultEventData, 
		setEventData: () => {},
});

function EventDashboard(){
    const [eventData, setEventData] = useState(defaultEventData);

    useEffect( () => {
        getData("/data").then( (jsonData) => {
            setEventData(jsonData);
        })
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

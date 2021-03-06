import React from "react";
import { useState, useEffect, useContext } from "react";
import Group from "./Group";
import config from "../config.json";
import {getData} from "../contrib.js";
import _ from "lodash";
import Version from "./Version";
import styles from "./EventDashboard.module.css";
import {defaultEventData, EventContext, CredentialContext} from "../context";

function EventDashboard(){
    const [eventData, setEventData] = useState(defaultEventData);
    const { credential } = useContext(CredentialContext);
    const [ percent, setPercent ] = useState(100);
    const [ timeInterval, setTimeInterval] = useState(config.refreshInterval);

    useEffect( () => {
        let stepSize = 5000;
        const interval = setInterval(() => {
            setTimeInterval(timeInterval => timeInterval + stepSize );
        }, stepSize);
        return () => clearInterval(interval);
    });

    useEffect(() => {
        let percent = ( timeInterval / config.refreshInterval ) * 100;
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
            <div className={styles.wrapper} >
                <div className={styles.versionDash}>
                    {
                        (
                            () => {
                                let groupList = [];
                                return _.map(
                                    _.sortBy(
                                        _.filter(eventData.eventResource, (item) => item.config.versionTracking && item.resourceVersion), 
                                        (item) => { return item.displayName }),
                                    (eventSource) => {
                                        return <Version displayName={eventSource.displayName} version={eventSource.resourceVersion} resourceUrl={eventSource.resourceUrl} linkToTag={eventSource.config.versionLinkToTag} />
                                    })
                            }

                        )()
                    }
                </div>

                <div>
                    {
                        (
                            () => {
                                let groupList = [];
                                _.forEach(eventData.eventSource, function(eventSource) {
                                    let groupEvents = _.filter(eventData.eventResource, (item) => { return item.eventSource === eventSource["slug"] });
                                    groupList.push([ _.filter(groupEvents, (evt) => { return evt.eventHistory.length > 0}).length,  <Group displayName={eventSource.displayName} slug={eventSource.slug} events={groupEvents} /> ]);   
                                })
                                console.log(groupList);
                                return _.map(_.sortBy(groupList, (item) => item[0]), (item) => item[1]).reverse() ;
                            }

                        )()
                    }

                </div>
            </div>
        </EventContext.Provider>
  );
}

export default EventDashboard;

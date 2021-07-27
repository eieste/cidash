import React from "react";
import { useContext, useState } from "react";
import Card from "./Card";
import _ from "lodash";
import style from "./Group.module.css";
function Group({displayName, slug, events}){
    return (
        <>
            <div className={style.group}>
                <div className={style.groupHeadline} >
                    <h2>{displayName}</h2>
                </div>
                <div className={style.groupEvent}>

                {
                    events.length <= 0 ? 
                        <div className={style.groupNoEvent}> Es sind noch keine weiteren Events registriert </div> 
                    :
                        <div className={style.groupEventWrapper}>
                            {
                                ( 
                                () => {
                                    return _.map(_.sortBy(events, (item) => item.displayName), function(event_resource){
                                        let sortedEvent = _.sortBy(event_resource.eventHistory, function(o) { return Date.parse(o.timestamp); });
                                        let complexMessage = sortedEvent[0].complexMessage
                                        if(event_resource.config.allowMessageInherith){
                                            _.forEach(sortedEvent, (item) => {
                                                if(complexMessage == "" || complexMessage == null || complexMessage == "null"){
                                                    complexMessage = item.complexMessage;
                                                }
                                            });
                                        }

                                        let event = sortedEvent[0]; // _.maxBy(event_resource.eventHistory, function(o) { return Date.parse(o.timestamp); });
                                        return (
                                            <Card simpleState={event.simpleState}
                                                  complexState={event.complexState}
                                                  complexMessage={complexMessage} 
                                                  eventSourceUrl={event.eventSourceUrl}
                                                  displayName={event_resource.displayName}
                                                  timestamp={new Date(event.timestamp)}
                                                  config={event.config}
                                                  eventHistory={event_resource.eventHistory}
                                            />);
                                    });
                                })()
                            }

                        </div>


                    }

                </div>
	    </div>
        </>
  );
}

export default Group;

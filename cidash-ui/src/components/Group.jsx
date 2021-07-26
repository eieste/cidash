import React from "react";
import { useContext, useState } from "react";
import Card from "./Card";
import _ from "lodash";


function Group({displayName, slug, events}){
    return (
        <>
            <style jsx >{`

                .group {
                    padding: 0;
                    margin: 20px;
                }

                .group-headline {
                    margin: 5px 20px 5px 20px;
                    border-bottom: 2px solid white;
                }
                
                .group-event {
                    margin: 20px;

                }
                .group-event-wrapper {
                    display: grid;
                    grid-column-gap: 15px;
                    grid-row-gap: 15px;
                    width: 100%;
                    /*grid-template-columns: repeat(4, 1fr);*/
                    grid-template-columns: repeat(auto-fit, 400px); /* minmax(400px, 500px));*/
                }

                .group-no-events {
                    width: 100%;
                    margin: 50px;
                    font-size: 30px;
                    text-align: center;
                }
            `}</style>
            <div className="group">
                <div className="group-headline">
                    <h2>{displayName}</h2>
                </div>
                <div className="group-event">

                {
                    events.length <= 0 ? 
                        <div className="group-no-events"> Es sind noch keine weiteren Events registriert </div> 
                    :
                        <div className="group-event-wrapper">
                            {
                                ( 
                                () => {
                                    return _.map(events, function(event_resource){
                                        let event = _.maxBy(event_resource.eventHistory, function(o) { return Date.parse(o.timestamp); });
                                        let asdf = new Date(event_resource.timestamp);
                                        return (
                                            <Card simpleState={event.simpleState}
                                                  complexState={event.complexState}
                                                  complexMessage={event.complexMessage} 
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

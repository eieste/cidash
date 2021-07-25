import React from "react";

function Card({ simpleState, complexState, complexMessage, displayName, eventSourceUrl, config, eventHistory, timestamp }){
    return (
        <> 
            <style jsx>{`
                .card {
                  font-size: 15px;
                  height: 180px;
                  border-radius: 10px;
                  color: white;
                  min-width: 400px;
                  transition: all .1s ease-in-out;
                  display: grid;
                  grid-template-columns: 1fr;
                  grid-template-rows: 1fr 1px 1fr 1px 1fr;
                }
                
                .card:hover{
                    transform: scale(1.05);
                -webkit-box-shadow: 0px 0px 23px 5px rgba(0,0,0,0.7); 
box-shadow: 0px 0px 23px 5px rgba(0,0,0,0.7);
                }

                .state-unknown {
                  background-color: #a6a6a6;
                }

                .state-information {
                  background-color: #3ca2de;
                }

                .state-okay {
                  background-color: #47c421;
                }

                .state-warning {
                  background-color: #ffb71c;
                }

                .state-error {
                  background-color: #ff6347; /*#ed2d40;*/
                }

                .card-head, .card-mid, .card-bottom {
                  display: grid;
                  padding: 15px;
                  grid-template-columns: 1fr 1fr;
                  grid-row-gap: 15px;
                }

                .card-seperator {
                  height:1px;
                  background-color: lightgray; 
                  margin: 0 30px 0 30px ;
                  right: 10px;
                  left: 0px;
                }

/*
                .simpleState {
                    font-size: 20px;
                    font-weight: bold;
                    cursor: pointer;
                }*/

            `}</style>
            <div className={"card state-"+simpleState}>
                <div class="card-head">
                    <div>
                        <span title={simpleState} alt={simpleState} className="simpleState">
                        {

                            (() => {
                                switch(simpleState){
                                
                                    case "okay":
                                        return "✓";
                                    break;
                                    
                                    case "information":
                                        return "🛈";
                                    break;

                                    case "pending":
                                        return "🗘";
                                    break;

                                    case "unknown":
                                        return "？";
                                    break;
                                    
                                    case "warning":
                                        return "⚠";
                                    break;

                                    case "error":
                                        return "🚫";
                                    break;
                                }
                            })()
                        }
                        </span>
                      </div>
                    <div>
                        <b>{displayName}</b>
                    </div>
                </div>
                <div className="card-seperator"/>
                <div class="card-mid">
                    <div>
                        {complexState}
                    </div>
                    <div>
                        {complexMessage}
                    </div>
                </div>
                <div className="card-seperator"/>
                <div class="card-bottom">
                    <div>
                        {timestamp.toLocaleString()}
                    </div>
                    <div>
                        { eventSourceUrl ? <a href={eventSourceUrl}>Resource </a> : ""}
                        { eventHistory.length <= 0 ? <a href="#">History</a> : ""}
                    </div>
                </div>
            </div>
        </>
  );
}

export default Card;

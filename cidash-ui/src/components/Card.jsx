import React from "react";
import styles from "./Card.module.css";

function Card({ simpleState, complexState, complexMessage, displayName, eventSourceUrl, config, eventHistory, timestamp }){

    if(simpleState == "pending"){
        simpleState = "information";
    }

    return (
        <> 
            <div className={[styles.card, styles["state-"+simpleState]].join(" ")}>
                <div className={styles.cardHead}>
                    <div>
                        <span title={simpleState} alt={simpleState} className={styles.simpleState} >
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
                <div className={styles.cardSeperator} />
                <div className={styles.cardMid}>
                    <div>
                        {complexState}
                    </div>
                    <div>
                        {complexMessage}
                    </div>
                </div>
                <div className={styles.cardSeperator} />
                <div className={styles.cardBottom}>
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

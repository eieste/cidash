import React, { useState } from "react";
import styles from "./Card.module.css";
import Modal from 'react-modal';
import _ from "lodash";
Modal.setAppElement('#root');

function Card({ simpleState, complexState, complexMessage, displayName, eventSourceUrl, config, eventHistory, timestamp }){

    const [modalIsOpen, setIsOpen] = useState(false);

    if(simpleState == "pending"){
        simpleState = "information";
    }


    function openModal() {
        setIsOpen(true);
    }

    function closeModal() {
        setIsOpen(false);
    }

    const customStyles = {
      content: {
        top: '50%',
        left: '50%',
        right: 'auto',
        bottom: 'auto',
        color: 'black',
        marginRight: '-50%',
        transform: 'translate(-50%, -50%)',
      },
    };

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
                                        return '\u2714';
                                    
                                    case "information":
                                        return '\u2139';

                                    case "pending":
                                        return '\u27F3';

                                    case "unknown":
                                        return '\u003F';
                                    
                                    case "warning":
                                        return '\u26A0';

                                    case "error":
                                        return '\u2297';

                                    default:
                                        return "???"

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
                    <div title={complexState}>
                        {complexState}
                    </div>
                    <div title={complexMessage}>
                        {complexMessage}
                    </div>
                </div>
                <div className={styles.cardSeperator} />
                <div className={styles.cardBottom}>
                    <div>
                        {timestamp.toLocaleString()}
                    </div>
                    <div className={styles.cardBottomLink}>
                        { eventSourceUrl ? <a target="_blank" href={eventSourceUrl}>Resource </a>: ""}
                        { eventSourceUrl && eventHistory.length >0 ? "  |  " : ""}
                        { eventHistory.length > 0 ? <span className={styles.link} onClick={openModal}>History</span> : ""}
                    </div>
                </div>
            </div>

            <Modal
            isOpen={modalIsOpen}
            onRequestClose={closeModal}
            style={customStyles}
            contentLabel="Example Modal"
            >
                <h2>History</h2>
                <button onClick={closeModal}>close</button>
                <table>
                    <tr>
                        <th>
                            State
                        </th>
                        <th>
                            Message
                        </th>
                        <th>
                            Timestamp
                        </th>
                        <th>
                            Url
                        </th>
                    </tr>

                    {
                        (
                            () =>{

                                return _.map(eventHistory, (event) => {
                                    return (<tr>
                                        <td>
                                            {event.complexState}
                                        </td>
                                        <td>
                                            {event.complexMessage}
                                        </td>
                                        <td>
                                            {event.timestamp.toLocaleString()}
                                        </td>
                                        <td>
                                            <a href={event.eventSourceUrl}>Resource</a>
                                        </td>
                                    </tr>)
                                });

                            }
                        )()
                    }

                </table>
            </Modal>
        </>
  );
}

export default Card;

import React from "react";
import styles from "./Version.module.css";

function Version({ displayName, version } ) {


    return <>
        <a href="https://github.com" className={styles.versionCard}>
            <div className={styles.versionTag}>
                {version}
            </div>
            <div className={styles.versionSeperator} />
            <div className={styles.versionPackageName}>
                {displayName} 
            </div>
        </a>

    </>;

}

export default Version;

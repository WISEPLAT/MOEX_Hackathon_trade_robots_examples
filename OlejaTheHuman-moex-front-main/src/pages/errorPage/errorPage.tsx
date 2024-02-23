import React from "react";
import styles from './error-page.module.css';

export default function ErrorPage(){
    return(
        <div className={styles.wrapper}>
            <span className={styles.emoji}>
                😿
            </span>
            <h1>Что-то пошло не так</h1>
        </div>
    );
}
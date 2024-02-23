import React from "react";
import styles from './header.module.css';
import {Link} from "react-router-dom";

export default function Header() {
    return (
        <header className={styles.wrapper}>
            <Link className={styles.title} to={'/'}>
                <span>Penix</span>
                <span>Long Short</span>
            </Link>
        </header>
    );
}
import React from "react";
import {useMatches} from "react-router";
import styles from './breadcrums.module.css';

export default function Breadcrumbs() {
    let matches = useMatches();
    let crumbs = matches
        // first get rid of any matches that don't have handle and crumb
        //@ts-ignore
        .filter((match) => Boolean(match.handle?.crumb))
        // now map them into an array of elements, passing the loader
        // data to each one
        //@ts-ignore
        .map((match) => match.handle.crumb(match.data));

    return (
        <ol>
            {crumbs.map((crumb, index) => (
                <li key={index}>{crumb}</li>
            ))}
        </ol>
    );
}
import React, {useEffect, useState} from "react";
import styles from './main-page.module.css';
import {Link} from "react-router-dom";
import {Header} from "../../components";
import {FileUploadItem} from "@alfalab/core-components/file-upload-item";
import {AllAlgosRequestT} from "../../types /types";
import {getAllDatasets} from "../../api/api";
import {Skeleton} from "@alfalab/core-components/skeleton";


export default function MainPage() {
    const [algos, setAlgos] = useState<AllAlgosRequestT>([]);
    const [datasetsLoading, setDatasetsLoading] = useState<boolean>(true);

    useEffect(() => {
        getAllDatasets().then(res => {
            setAlgos(res);
            setDatasetsLoading(false);
        })
    }, []);

    return (
        <>
            <Header/>
            <div className={styles.wrapper}>
                <div className={styles.uploadedData}>
                    <div className={styles.header}>
                        <div>
                            <div className={styles.title}>Загруженные алгоритмы</div>
                            <p>Выберите нужный алгоритм</p>
                        </div>
                    </div>
                    <div className={styles.algosList}>
                        {algos.map((algo, index) =>
                            <div
                                className={styles.fileUploadItem}
                                key={index}
                            >
                                <Link to={`/algos/${algo}`}>
                                    <FileUploadItem
                                        name={algo ?? ''}
                                        showDelete={false}
                                        showRestore={false}
                                    />
                                </Link>
                            </div>
                        )}
                        {
                            datasetsLoading ?
                                <React.Fragment>
                                    <Skeleton visible={datasetsLoading}>
                                        <div className={styles.skeleton}></div>
                                    </Skeleton>
                                    <Skeleton visible={datasetsLoading}>
                                        <div className={styles.skeleton}></div>
                                    </Skeleton>
                                </React.Fragment>
                                : null
                        }
                    </div>
                </div>
            </div>
        </>
    );
}
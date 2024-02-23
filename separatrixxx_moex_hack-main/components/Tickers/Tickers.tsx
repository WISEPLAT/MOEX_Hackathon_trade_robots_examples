import styles from './Tickers.module.css';
import { useRouter } from 'next/router';
import Link from 'next/link';
import { useState } from 'react';
import { Htag } from 'components/Htag/Htag';
import { Modal } from 'components/Modal/Modal';
import { useDispatch, useSelector } from 'react-redux';
import { AppState } from 'features/store/store';
import { setTicker } from 'features/ticker/tickerSlice';


export const Tickers = (): JSX.Element => {
    const router = useRouter();
    const dispatch = useDispatch();

    const [active, setActive] = useState<boolean>(false);

    const ticker = useSelector((state: AppState) => state.ticker.ticker);

    const tickers = ['AAPL', 'MOEX', 'SBER', 'TSLA', 'MSFT'];

    return (
        <>
            <Htag tag='xs' className={styles.ticker} onClick={() => setActive(true)}>
                {ticker}
            </Htag>
            <Modal active={active} setActive={setActive}>
                <div className={styles.blockTickers}>
                    {tickers.map(t => (
                        <Link key={t} href={router.asPath} className={styles.tickerBlock}
                            onClick={() => {
                                dispatch(setTicker(t));
                                setActive(false);
                            }}>
                            <span className={styles.logo} />
                            <Htag tag='s' className={styles.tickerLink}>{t}</Htag>
                        </Link>
                    ))}
                </div>
            </Modal>
        </>
    );
};
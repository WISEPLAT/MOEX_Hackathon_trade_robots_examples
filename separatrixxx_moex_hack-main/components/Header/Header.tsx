import styles from './Header.module.css';
import { LocaleChange } from 'components/LocaleChange/LocaleChange';
import { Tickers } from 'components/Tickers/Tickers';


export const Header = (): JSX.Element => {
	return (
        <header className={styles.header}>
            <Tickers />
            <LocaleChange />
        </header>
    );
};

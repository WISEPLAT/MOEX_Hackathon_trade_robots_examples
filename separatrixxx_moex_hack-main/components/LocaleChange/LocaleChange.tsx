import styles from './LocaleChange.module.css';
import { useRouter } from 'next/router';
import Link from 'next/link';
import { useState } from 'react';
import { en } from 'locales/en.locale';
import { ru } from 'locales/ru.locale';
import { setLocale } from 'helpers/locale.helper';
import { Htag } from 'components/Htag/Htag';
import { Modal } from 'components/Modal/Modal';


export const LocaleChange = (): JSX.Element => {
    const router = useRouter();

    const [active, setActive] = useState<boolean>(false);

    const languages = [en, ru];
    const langIndex = languages.indexOf(setLocale(router.locale));

    if (langIndex !== -1) {
        languages.splice(langIndex, 1);
    }

    return (
        <>
            <Htag tag='xs' className={styles.lang} onClick={() => setActive(true)}>
                {setLocale(router.locale).lang}
            </Htag>
            <Modal active={active} setActive={setActive}>
                <div className={styles.blockLanguages}>
                    {languages.map(l => (
                        <Link key={l.locale} href={router.asPath} locale={l.locale}
                            onClick={() => setActive(false)}>
                            <Htag tag='s' className={styles.langLink}>{l.language}</Htag>
                        </Link>
                    ))}
                </div>
            </Modal>
        </>
    );
};
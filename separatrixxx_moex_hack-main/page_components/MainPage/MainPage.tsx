import styles from './MainPage.module.css';
import { Toaster } from 'react-hot-toast';
import { useRouter } from 'next/router';
import { Header } from 'components/Header/Header';
import { GraphicBlock } from 'components/GraphicBlock/GraphicBlock';
import { NewsBlock } from 'components/NewsBlock/NewsBlock';


export const MainPage = (): JSX.Element => {
    const router = useRouter();

    return (
        <>
            <Toaster
				position="top-center"
				reverseOrder={true}
				toastOptions={{
					duration: 2000,
				}}
			/>
            <div className={styles.wrapper}>
                <Header />
                <div className={styles.blocks}>
                    <GraphicBlock />
                    <NewsBlock />
                </div>
            </div>
        </>
    );
};
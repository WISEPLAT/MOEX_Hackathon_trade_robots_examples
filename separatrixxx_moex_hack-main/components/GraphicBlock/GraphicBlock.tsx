import styles from './GraphicBlock.module.css';
import { useSelector } from 'react-redux';
import { AppState } from 'features/store/store';
import { getCandles, getNowPrice } from 'helpers/candles.helper';
import { useState } from 'react';
import { CandleInterface } from 'interfaces/candle.interface';
import { VictoryChart, VictoryLine, VictoryTheme } from 'victory';
import { Htag } from 'components/Htag/Htag';
import { Modal } from 'components/Modal/Modal';
import { useRouter } from 'next/router';
import { setLocale } from 'helpers/locale.helper';
import { TimeInterface } from 'interfaces/time.interface';
   

export const GraphicBlock = (): JSX.Element => {
  const router = useRouter();
  
    const ticker = useSelector((state: AppState) => state.ticker.ticker);

    const [active, setActive] = useState<boolean>(false);
    const [candles, setCandles] = useState<CandleInterface[]>([]);
    const [nowPrice, setNowPrice] = useState<number>(0);
    const [time, setTime] = useState<'M' | 'D' | 'h'>('D');

    const times: TimeInterface[] = [
      {full: setLocale(router.locale).month, short: 'M'},
      {full: setLocale(router.locale).day, short: 'D'},
      {full: setLocale(router.locale).hour, short: 'h'}
    ]
    
    getCandles(ticker, time, setCandles);
    getNowPrice(ticker, setNowPrice);

  return (
        <>
          <div className={styles.graphicBlock}>
            <div className={styles.optionsDiv}>
              <Htag tag='s' className={styles.title}>SBERBANK</Htag>
              <span className={styles.circle} />
              <Htag tag='s' className={styles.time} onClick={() => setActive(true)}>
                {time}
              </Htag>
              <Htag tag='s'>{nowPrice}</Htag>
            </div>
            <VictoryChart
              theme={VictoryTheme.material}
            >
              <VictoryLine
                style={{
                  data: { stroke: "#c43a31" },
                  parent: { border: "1px solid #ccc"}
                }}
                // data={[
                //   { x: 1, y: 2 },
                //   { x: 2, y: 3 },
                //   { x: 3, y: 5 },
                //   { x: 4, y: 4 },
                //   { x: 5, y: 7 }
                // ]}
                data={
                  candles.map(
                    c => (
                      {
                        x: c.begin.slice(5, 7),
                        y: c.high 
                      }
                    )
                  )
                }
              />
            </VictoryChart>
          </div>
          <Modal active={active} setActive={setActive}>
            <div className={styles.blockLanguages}>
              {times.map(t => (
                <Htag key={t.full} tag='s' className={styles.times} onClick={() => {
                  setTime(t.short);
                  setActive(false);
                }}>
                  {t.full}
                </Htag>
              ))}
            </div>
          </Modal>
        </>
    );
};

import React, { FC, PropsWithChildren } from 'react';
import styles from './client_message.module.css';

const ClientMessage: FC<PropsWithChildren<{time: string}>> = ({children, time}) => {
  return (
    <div className={styles.client_message}>
      {children}
      <span className={styles.time}>{time}</span>
    </div>
  );
}

export default ClientMessage;
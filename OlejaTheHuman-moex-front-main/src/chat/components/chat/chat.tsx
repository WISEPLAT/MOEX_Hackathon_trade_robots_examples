import React, { FC, PropsWithChildren } from 'react';
import styles from './chat.module.css';

const Chat: FC<PropsWithChildren> = ({children}) => {
  return (
    <div className={styles.wrapper}>
      {children}
    </div>
  );
}

export default Chat;
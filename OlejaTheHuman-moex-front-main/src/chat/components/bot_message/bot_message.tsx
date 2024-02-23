import React, { FC, PropsWithChildren } from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';

import styles from './bot_message.module.css';


const BotMessage: FC<PropsWithChildren<{ time: string, message: string }>> = ({ time, message, children}) => {
  return (
    <div className={ styles.bot_message }>
      <ReactMarkdown className={styles.markdown} children={ message } remarkPlugins={[remarkGfm]}/>
      <span className={ styles.time }>{ time }</span>
      {children}
    </div>
  )
}

export default BotMessage;
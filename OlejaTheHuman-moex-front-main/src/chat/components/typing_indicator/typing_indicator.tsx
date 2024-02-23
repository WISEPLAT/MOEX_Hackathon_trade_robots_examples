import React from 'react';
import styles from './typing_indicator.module.css'

const TypingIndicator = () => {
  return (
    <div className={ styles.wave }>
      <span className={ styles.dot }/>
      <span className={ styles.dot }/>
      <span className={ styles.dot }/>
    </div>
  );
}

export default TypingIndicator;
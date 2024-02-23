import React, { FunctionComponent } from 'react';
import styles from './send-button.module.css';
import sendIcon from './send.svg';


interface PropsI {
  onClick?: () => void
}


const SendButton: FunctionComponent<PropsI> = (props) => {

  return (
    <div onClick={ props.onClick } className={ styles.wrapper }>
      <img src={ sendIcon } alt="send"/>
    </div>
  );
}

export default SendButton;
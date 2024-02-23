import React, {JSXElementConstructor, useEffect, useRef} from 'react';

import {BotMessage, Chat, ClientMessage, InputMessage, TypingIndicator} from './components'
import styles from './chat.module.css';
import {useSelector} from 'react-redux';
import {RootState} from './store/store';
import {formatAMPM} from '../utils/am-pm-formatter';
import {ClientMessageI} from './store/types';
import {CrossHeavyMIcon} from '@alfalab/icons-glyph/CrossHeavyMIcon';
import {IconButton} from "@alfalab/core-components/icon-button";


const Message: JSXElementConstructor<ClientMessageI> = (message: ClientMessageI, index: number) => {
    if (message.type === 'client') {
        return (
            <ClientMessage
                time={formatAMPM(message.date)}
                key={`${message.content}_${index}`}
            >
                {message.content}
            </ClientMessage>
        );
    } else if (message.type === 'bot' || message.type === 'error') {
        return (
            <BotMessage
                time={formatAMPM(message.date)}
                message={message.content}
                key={`${message.content}_${index}`}
            />
        );
    }
    return (
        <BotMessage
            time={formatAMPM(message.date)}
            message={message.content}
            key={`${message.content}_${index}`}
        >
            <TypingIndicator/>
        </BotMessage>
    );
}

export interface AlphaChatPropsI {
    onClose?: () => void;
    open: boolean;
}

function AlphaChat({onClose, open}: AlphaChatPropsI) {
    const chat = useRef<HTMLInputElement>(null);
    const messages = useSelector((state: RootState) => state.messagesReducer.messages)

    useEffect(() => {
        chat.current?.scrollTo({top: chat.current.scrollHeight});
    }, [messages]);

    useEffect(() => {
        if(open) {
            document.body.style.overflow = 'hidden';
        } else {
            document.body.style.overflow = 'unset';
        }
    }, [open]);

    useEffect(() => {
        return () => {document.body.style.overflow = 'unset'}
    }, []);

    return (
        <>
            {
                open ?
                    <div className={styles.wrapper}>
                        <Chat>
                            <div className={styles.header}>
                                <h1>Подручный на связи</h1>
                                <IconButton
                                    view='primary'
                                    size='xs'
                                    icon={CrossHeavyMIcon}
                                    onClick={() => {
                                        onClose?.();
                                    }}
                                />
                            </div>
                            <main ref={chat} className={styles.content}>
                                {
                                    // @ts-ignore
                                    messages.map((msg, index) => Message(msg, index))
                                }
                            </main>
                            <InputMessage/>
                        </Chat>
                    </div> : null
            }

        </>
    );
}

export default AlphaChat;

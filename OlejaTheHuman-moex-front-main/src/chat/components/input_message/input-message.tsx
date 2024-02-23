import React, {FormEvent, FunctionComponent, KeyboardEvent, useEffect, useRef, useState} from 'react';
import {useDispatch} from 'react-redux'
import {useLocation} from 'react-router-dom';
import {SendButton} from '../../components';
import styles from './input.module.css';
import {usePostMessageMutation} from '../../store/api';
import {addMessage, setBotTyping, setBotTypingEnd, setError} from '../../store/reducers';
import {MessageI} from "../../store/types";

const InputMessage: FunctionComponent = () => {
    const [postMessage] = usePostMessageMutation()
    const textArea = useRef(null);
    const [inputValue, setInputValue] = useState('');
    const dispatch = useDispatch()
    const currentLocation = useLocation();

    function addNewMessage() {
        if (inputValue.length === 0) return;

        dispatch(addMessage({
            type: 'client',
            content: inputValue,
            date: new Date(),
        }));
        dispatch(setBotTyping());

        postMessage({
            dataset_id: currentLocation.pathname.split('/')[2],
            user_query: inputValue,
        })
            .unwrap()
            .then((resp: MessageI) => {
                if(typeof resp !== 'string') throw new Error('resp is not a string');
                dispatch(addMessage({
                    type: 'bot',
                    content: resp,
                    date: new Date(),
                }));
                dispatch(setBotTypingEnd());
            })
            .catch(err => {
                console.error(err)
                dispatch(setBotTypingEnd());
                dispatch(setError())
            });

        setInputValue('');
    }

    function onEnterPress(e: KeyboardEvent) {
        if (e.key !== 'Enter') return;
        addNewMessage();
        e.preventDefault();
        //@ts-ignore
        textArea.current.style.height = "auto";
    }

    function submit(event: FormEvent<HTMLFormElement>) {
        event.preventDefault();
        addNewMessage();
        //@ts-ignore
        textArea.current.style.height = "auto";
    }

    const resizeArea = (e: FormEvent<HTMLTextAreaElement>) => {
        //@ts-ignore
        e.target.style.height = "auto";
        //@ts-ignore
        e.target.style.height = e.target.scrollHeight + "px";
    }

    return (
        <div className={styles.wrapper}>
            <form className={styles.form} onSubmit={submit}>
        <textarea
            rows={1}
            ref={textArea}
            className={styles.input}
            value={inputValue}
            onInput={(e) => resizeArea(e)}
            placeholder="Start typing..."
            onChange={(e) => setInputValue(e.target.value)}
            onKeyDown={onEnterPress}
        />
                <label>
                    <SendButton/>
                    <input style={{display: 'none'}} type="submit" value="Submit"/>
                </label>
            </form>
        </div>
    );
}

export default InputMessage;
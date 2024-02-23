import type { PayloadAction } from '@reduxjs/toolkit';
import { createSlice } from '@reduxjs/toolkit';
import { ClientMessageI } from './types';


export interface MessagesStateI {
  messages: ClientMessageI[];
}


const initialState: MessagesStateI = {
  messages: [],
}

export const messagesSlice = createSlice({
  name: 'messages',
  initialState,
  reducers: {
    addMessage: (state, action: PayloadAction<ClientMessageI>) => {
      state.messages.push(action.payload);
    },
    setBotTyping: (state) => {
      state.messages.push({
        type: 'typing',
        date: new Date(),
        content: '',
      })
    },
    setBotTypingEnd: (state) => {
      state.messages = state.messages.filter(message => message.type !== 'typing');
    },
    setError: (state) => {
      state.messages.push({
        type: 'error',
        date: new Date(),
        content: "Sorry, I'm having an issue responding to you. Please try one more time."
      })
    }
  },
})

export const {addMessage, setBotTyping, setBotTypingEnd, setError} = messagesSlice.actions
export default messagesSlice.reducer
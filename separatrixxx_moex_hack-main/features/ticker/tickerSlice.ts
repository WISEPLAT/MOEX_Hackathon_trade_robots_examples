import { createSlice } from '@reduxjs/toolkit'


export const tickerSlice = createSlice({
  name: 'ticker',
  initialState: {
    ticker: 'SBER',
  },
  reducers: {
    setTicker: (state, actions) => {
        state.ticker = actions.payload
    },
  },
})

export const { setTicker } = tickerSlice.actions

export default tickerSlice.reducer;
import '../styles/globals.css';
import type { AppProps } from 'next/app';
import Head from 'next/head';
import React from 'react';
import { wrapper } from 'features/store/store';
import { Provider } from 'react-redux';


export default function App({ Component, pageProps }: AppProps) {
  const { store } = wrapper.useWrappedStore(pageProps);

  return (
    <Provider store={store}>
      <Head>
        <title>MOEX Hack</title>
        <meta name='description' content='MOEX Hack' />
        <meta property='og:title' content='MOEX Hack' />
        <meta property='og:description' content='MOEX Hack' />
        <meta charSet="utf-8" />
        <link rel="icon" href="/vercel.svg" type='image/svg+xml' />
      </Head>
      <Component {...pageProps} />
    </Provider>

  );
}

import { NextPageContext } from 'next';
import { getSession, SessionProvider } from 'next-auth/react';
import type { AppProps } from 'next/app';

import '../styles/global.scss';

export const getServerSideProps = async (context: NextPageContext) => {
  return {
    props: {
      session: await getSession(context),
    },
  };
};

function MyApp({ Component, pageProps }: AppProps) {
  return (
    <>
      <SessionProvider session={pageProps.session} refetchInterval={0}>
        <Component {...pageProps} />
      </SessionProvider>
    </>
  );
}

export default MyApp;

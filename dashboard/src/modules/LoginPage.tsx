import { Button } from '../ui/Button';
import { CenterLayout } from '../ui/layouts/CenterLayout';
import { signIn, signOut, useSession } from 'next-auth/react';
import { useRouter } from 'next/router';
import { useEffect } from 'react';

export const LoginPage = () => {
  const { data: session } = useSession();
  const { push } = useRouter();

  // if (typeof window !== 'undefined' && loading) return null;

  // You can pretty much do the same with getServerSideProps but
  // I don't want to put much code in "src/pages" files.
  useEffect(() => {
    if (session) {
      push('/');
    }
  }, [session, push]);

  return (
    <CenterLayout>
      <h1 className="font-bold text-2xl">Log in Lol.</h1>
      {session && (
        <Button
          onClick={() => {
            signOut();
          }}
        >
          Sign out
        </Button>
      )}
      {!session && (
        <Button
          onClick={() => {
            signIn('google');
          }}
        >
          Sign in
        </Button>
      )}
      <p>{session?.user?.email}</p>
    </CenterLayout>
  );
};

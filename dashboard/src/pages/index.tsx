import { useSession } from 'next-auth/react';
import { CenterLayout } from '../ui/layouts/CenterLayout';

export default function Home() {
  const { data: session } = useSession();

  return (
    <CenterLayout>
      <h1 className={`text-2xl font-bold`}>Hi! This is your first app.</h1>
      <p>
        There&apos;s some elements in the <kbd>/ui</kbd> directory you can use,
        check it out!
      </p>
      <p>{session?.user?.email}</p>
    </CenterLayout>
  );
}

// export const getServerSideProps = async (context: NextPageContext) => {
//   return {
//     props: {},
//   };
// };

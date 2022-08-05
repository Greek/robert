import Image from 'next/image';

import { useSession } from 'next-auth/react';
import { useRouter } from 'next/router';
import { useEffect } from 'react';
import { DashLayout } from '../../ui/layouts/DashLayout';

interface TlxDataViewProps {
  children: React.ReactNode;
}

export const TlxDataView: React.FC<TlxDataViewProps> = ({ children }) => {
  const { push } = useRouter();
  const { id } = useRouter().query;
  const session = useSession();

  useEffect(() => {
    // eslint-disable-next-line @typescript-eslint/ban-ts-comment
    /* @ts-ignore */
    if (!session.data?.user?.email == 'apapuig+discord@gmail.com') push('/');
    if (!session) push('/login');
  }, [session, push]);

  return (
    <DashLayout title={`TLX / ${id}`}>
      <div className={`px-4 py-4`}>
        <div className={`flex flex-row gap-2`}>
          <Image
            src={`https://cdn.discordapp.com/icons/989659178178068521/7039e3606ea2fd722127efd121586591.png?size=128`}
            width={40}
            height={16}
            className={`rounded-full border-2 border-zinc-600`}
            alt="Guild icon"
          />
          <p className={`text-4xl`}>Guild Name</p>
        </div>
      </div>
    </DashLayout>
  );
};

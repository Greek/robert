import Image from 'next/image';

import { useSession } from 'next-auth/react';
import { useRouter } from 'next/router';
import { useEffect } from 'react';
import { DashLayout } from '../../ui/layouts/DashLayout';
import useSWR from 'swr';
import prisma from '../../lib/prisma';
import { NextPageContext } from 'next';
import fetcher from '../../lib/fetcher';
import { TLXReport } from '@prisma/client';
import { CenterLayout } from '../../ui/layouts/CenterLayout';

interface TlxDataViewProps {
  children: React.ReactNode;
}

export const TlxDataView: React.FC<TlxDataViewProps> = ({
  children,
  ...props
}) => {
  const { push } = useRouter();
  const { id } = useRouter().query;
  const session = useSession();

  useEffect(() => {
    // eslint-disable-next-line @typescript-eslint/ban-ts-comment
    /* @ts-ignore */
    if (!session.data?.user?.email == 'apapuig+discord@gmail.com') push('/');
    if (!session) push('/login');
  }, [session, push]);

  const { data } = useSWR(`/api/tlx/report/${id}`, fetcher, {});
  const report: TLXReport = data?.result;

  if (!report) {
    return (
      <DashLayout title="TLX / Not Found">
        <div className={`flex items-center justify-center h-[90vh]`}>
          This TLX report could not be loaded.
        </div>
      </DashLayout>
    );
  }

  return (
    <DashLayout title={`TLX / ${id}`}>
      <div className={`px-4 py-4`}>
        <div className={`flex flex-row gap-2`}>
          <Image
            src={`${report.icon}`}
            width={40}
            height={16}
            className={`rounded-full border-2 border-zinc-600`}
            alt="Guild icon"
          />
          <p className={`text-4xl`}>{report.name}</p>
        </div>
      </div>
    </DashLayout>
  );
};

import { useSession } from 'next-auth/react';
import { useRouter } from 'next/router';
import { useEffect } from 'react';
import { DashLayout } from '../../ui/layouts/DashLayout';

interface TlxDataViewProps {
  children: React.ReactNode;
}

export const TlxDataView: React.FC<TlxDataViewProps> = ({ children }) => {

  const router = useRouter();
  const session = useSession();
  const { id } = router.query;


  useEffect(() => {
    if (!session.data?.user?.email == "apapuig+discord@gmail.com")
        router.push('/')
    if (!session) router.push('/login')
    
  }, [session, router])

  return <DashLayout>TLX ID: {id}</DashLayout>;
};

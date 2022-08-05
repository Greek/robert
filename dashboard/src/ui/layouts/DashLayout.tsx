import { Sidebar } from '../Sidebar';

export interface DashLayoutProps {
  children?: React.ReactNode;
}

export const DashLayout: React.FC<DashLayoutProps> = ({ children }) => {
  return (
    <div>
      <Sidebar />
      <div className={`ml-[17rem]`}>{children}</div>
    </div>
  );
};

import { Sidebar } from '../Sidebar';

export interface DashLayoutProps {
  children?: React.ReactNode;
  title?: string;
}

export const DashLayout: React.FC<DashLayoutProps> = ({ children, title }) => {
  return (
    <div>
      <Sidebar />
      <div className={`ml-[17rem]`}>
        {title && (
          <div className={`w-full p-4 h-14 border-b-[1.4px] border-b-zinc-600`}>
            {title}
          </div>
        )}
        {children}
      </div>
    </div>
  );
};

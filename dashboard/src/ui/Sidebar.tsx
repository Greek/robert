import { SidebarItem } from './SidebarItem';

interface SidebarProps {
  children?: React.ReactNode;
}

export const LoadingSidebar: React.FC<Record<string, unknown>> = () => {
  return (
    <div
      className={`flex flex-col absolute min-h-screen max-w-[20rem] w-[17rem] h-screen border-r-zinc-600 border-r-[1.7px] items-center justify-center`}
    >
      <h1>Loading...</h1>
    </div>
  );
};

export const Sidebar: React.FC<SidebarProps> = ({ children }) => {
  return (
    <div
      className={`flex flex-col absolute min-h-screen max-w-[20rem] w-[17rem] h-screen border-r-zinc-600 border-r-[1.7px]`}
    >
      <div
        className={`flex flex-row items-center gap-x-2 h-14 border-b-[1.7px] border-b-zinc-600 p-2`}
      >
        <h1>Hello!</h1>
      </div>
      {children}
      {/* {!posts && <p>Loading...</p>} */}

      <SidebarItem title="Hello!" content="This is the sidebar."></SidebarItem>
    </div>
  );
};

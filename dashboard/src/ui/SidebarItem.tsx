import Link from 'next/link';

interface SidebarItemProps {
  children?: React.ReactNode;
  title?: string;
  content?: string;
  lastEdited?: Date;
  id?: string;
}

export const SidebarItem: React.FC<SidebarItemProps> = ({
  title = 'Hello world!',
  content = 'Content.',
  id,
}) => {
  return (
    <Link href={`/post/${id}`}>
      <div
        className={`hover:bg-button-bg transition ease-out hover:cursor-pointer border-b-[1.7px] border-b-zinc-600 p-3 text-xl`}
      >
        <p className={`font-semibold`}>{title}</p>
        <p className={`${'font-normal text-xs'}`}>{content}</p>
      </div>
    </Link>
  );
};

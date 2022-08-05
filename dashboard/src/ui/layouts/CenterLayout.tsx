const colorTheme = {
  dark: 'bg-layout-bg text-color-text',
  light: 'bg-layout-bg text-black',
};

export type CenterLayoutProps = React.DetailedHTMLProps<
  React.HTMLAttributes<HTMLDivElement>,
  HTMLDivElement
> & {
  theme?: keyof typeof colorTheme;
  // children?: React.ReactNode;
};

export const CenterLayout: React.FC<CenterLayoutProps> = ({
  theme = 'dark',
  children,
  ...props
}) => {
  return (
    <div
      className={`min-h-screen flex flex-col items-center justify-center ${colorTheme[theme]}`}
      {...props}
    >
      {children}
    </div>
  );
};

import { HtagProps } from './Htag.props';
import styles from './Htag.module.css';
import cn from 'classnames';


export const Htag = ({ tag, children, className, onClick }: HtagProps): JSX.Element => {
	switch (tag) {
		case 'xxl':
			return <h1 className={cn(className, styles.xxl)} onClick={onClick}>{children}</h1>;
		case 'xl':
			return <h1 className={cn(className, styles.xl)} onClick={onClick}>{children}</h1>;
		case 'l':
			return <h1 className={cn(className, styles.l)} onClick={onClick}>{children}</h1>;
		case 'm':
			return <h1 className={cn(className, styles.m)} onClick={onClick}>{children}</h1>;
		case 's':
			return <h2 className={cn(className, styles.s)} onClick={onClick}>{children}</h2>;
		case 'xs':
			return <h2 className={cn(className, styles.xs)} onClick={onClick}>{children}</h2>;
		case 'xxs':
			return <h3 className={cn(className, styles.xxs)} onClick={onClick}>{children}</h3>;
		default:
			return <></>;
	}
};
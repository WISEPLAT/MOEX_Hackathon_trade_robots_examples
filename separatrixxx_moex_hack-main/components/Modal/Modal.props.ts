import { ReactNode } from 'react';

export interface ModalProps {
	active: boolean,
	setActive: (e: any) => void,
	children: ReactNode,
}
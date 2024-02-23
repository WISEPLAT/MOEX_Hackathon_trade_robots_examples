import toast from 'react-hot-toast';

export const ToastSuccess = (message: string | undefined): void => {
    if (message) {
        toast.error(message, {
            icon: '🤩',
            style: {
                borderRadius: '9999px',
                color: 'var(--primary)',
            },
        });
    }
};

export const ToastError = (message: string | undefined): void => {
    if (message) {
        toast.error(message, {
            icon: '🙄',
            style: {
                borderRadius: '9999px',
                color: 'var(--error)',
            },
        });
    }
};
export function uploadFileHelper(callback?: (file: File) => void) {
    const element = document.createElement('input');
    element.setAttribute('type', 'file');
    element.setAttribute('accept', '.csv');
    // element.setAttribute('href', link);
    // element.setAttribute('download', 'Contact');
    element.style.display = 'none';

    document.body.appendChild(element);

    element.click();

    element.addEventListener('change', e => {
        if(!element.files) {
            document.body.removeChild(element);
            return;
        };
        callback?.(Array.from(element.files)[0])
    })
}
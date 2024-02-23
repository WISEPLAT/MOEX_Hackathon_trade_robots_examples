interface Mapping {
    [key: string]: string;
}

declare module '*.module.css' {
    const mapping: Mapping;
    export default mapping;
}
declare module '*.module.scss' {
    const mapping: Mapping;
    export default mapping;
}
declare module '*.module.sass' {
    const mapping: Mapping;
    export default mapping;
}
declare module '*.module.styl' {
    const mapping: Mapping;
    export default mapping;
}

declare module '*.svg?inline' {
    const content: any;
    export default content;
}

declare module '*.svg' {
    const content: string;
    export default content;
}

declare module '*.png' {
    const content: string;
    export default content;
}
declare module '*.jpg' {
    const content: string;
    export default content;
}
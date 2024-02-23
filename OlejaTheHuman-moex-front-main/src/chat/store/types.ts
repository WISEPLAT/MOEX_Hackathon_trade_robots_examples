export type MessageI = string;

export interface DatasetMessageI {
    dataset_id: string;
    user_query: string;
}

export interface ClientMessageI {
    type: 'bot' | 'client' | 'typing' | 'error'
    date: Date;
    content: string;
}